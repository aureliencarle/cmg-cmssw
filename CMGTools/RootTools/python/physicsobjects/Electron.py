from CMGTools.RootTools.physicsobjects.Lepton import Lepton
from CMGTools.RootTools.physicsobjects.ElectronMVAID import ElectronMVAID_Trig, ElectronMVAID_NonTrig, ElectronMVAID_TrigNoIP


class Electron( Lepton ):

    def __init__(self, *args, **kwargs):
        '''Initializing tightIdResult to None. The user is responsible
        for setting this attribute externally if he wants to use the tightId
        function.'''
        super(Electron, self).__init__(*args, **kwargs)
        self.tightIdResult = None
        self.associatedVertex = None
        self.rho              = None
        self._mvaNonTrigV0  = None
        self._mvaTrigV0     = None
        self._mvaTrigNoIPV0 = None

    def electronID( self, id, vertex=None, rho=None ):
        if id is None or id == "": return True
        if vertex == None and hasattr(self,'associatedVertex') and self.associatedVertex != None: vertex = self.associatedVertex
        if rho == None and hasattr(self,'rho') and self.rho != None: rho = self.rho
        if   id == "POG_MVA_ID_NonTrig":  return self.mvaIDLoose()
        elif id == "POG_MVA_ID_Trig":     return self.mvaIDTight()
        raise RuntimeError, "Electron id '%s' not yet implemented in Electron.py" % id

    def absEffAreaIso(self,rho,effectiveAreas):
        '''MIKE, missing doc.
        Should have the same name as the function in the mother class.
        Can call the mother class function with super.
        '''
        return self.absIsoFromEA(rho,self.superCluster().eta(),effectiveAreas.eGamma)

    def mvaId( self ):
        return self.mvaNonTrigV0()
        
    def tightId( self ):
        return self.tightIdResult
    
    def mvaNonTrigV0( self, debug = False ):
        if self._mvaNonTrigV0 == None:
            if self.associatedVertex == None: raise RuntimeError, "You need to set electron.associatedVertex before calling any MVA"
            if self.rho              == None: raise RuntimeError, "You need to set electron.rho before calling any MVA"
            self._mvaNonTrigV0 = ElectronMVAID_NonTrig(self.physObj, self.associatedVertex, self.rho, debug)
        return self._mvaNonTrigV0 

    def mvaTrigV0( self, debug = False ):
        if self._mvaTrigV0 == None:
            if self.associatedVertex == None: raise RuntimeError, "You need to set electron.associatedVertex before calling any MVA"
            if self.rho              == None: raise RuntimeError, "You need to set electron.rho before calling any MVA"
            self._mvaTrigV0 = ElectronMVAID_Trig(self.physObj, self.associatedVertex, self.rho, debug)
        return self._mvaTrigV0 

    def mvaTrigNoIPV0( self, debug = False ):
        if self._mvaTrigNoIPV0 == None:
            if self.associatedVertex == None: raise RuntimeError, "You need to set electron.associatedVertex before calling any MVA"
            if self.rho              == None: raise RuntimeError, "You need to set electron.rho before calling any MVA"
            self._mvaTrigNoIPV0 = ElectronMVAID_TrigNoIP(self.physObj, self.associatedVertex, self.rho, debug)
        return self._mvaTrigNoIPV0 


    def mvaIDTight(self):
            eta = abs(self.superCluster().eta())
            if self.pt() < 20:
                if   (eta < 0.8)  : return self.mvaTrigV0() > +0.00;
                elif (eta < 1.479): return self.mvaTrigV0() > +0.10;
                else              : return self.mvaTrigV0() > +0.62;
            else:
                if   (eta < 0.8)  : return self.mvaTrigV0() > +0.94;
                elif (eta < 1.479): return self.mvaTrigV0() > +0.85;
                else              : return self.mvaTrigV0() > +0.92;

    def mvaIDLoose(self):
            eta = abs(self.superCluster().eta())
            if self.pt() < 10:
                if   (eta < 0.8)  : return self.mvaNonTrigV0() > +0.47;
                elif (eta < 1.479): return self.mvaNonTrigV0() > +0.004;
                else              : return self.mvaNonTrigV0() > +0.295;
            else:
                if   (eta < 0.8)  : return self.mvaNonTrigV0() > -0.34;
                elif (eta < 1.479): return self.mvaNonTrigV0() > -0.65;
                else              : return self.mvaNonTrigV0() > +0.60;

    def mvaIDZZ(self):
        return self.mvaIDLoose() and (self.gsfTrack().trackerExpectedHitsInner().numberOfLostHits()<=1)

    def chargedHadronIso(self,R=0.4):
        if   R == 0.3: return self.physObj.pfIsolationVariables().sumChargedHadronPt 
        elif R == 0.4: return self.physObj.chargedHadronIso()
        raise RuntimeError, "Electron chargedHadronIso missing for R=%s" % R

    def neutralHadronIso(self,R=0.4):
        if   R == 0.3: return self.physObj.pfIsolationVariables().sumNeutralHadronEt 
        elif R == 0.4: return self.physObj.neutralHadronIso()
        raise RuntimeError, "Electron neutralHadronIso missing for R=%s" % R

    def photonIso(self,R=0.4):
        if   R == 0.3: return self.physObj.pfIsolationVariables().sumPhotonEt 
        elif R == 0.4: return self.physObj.photonIso()
        raise RuntimeError, "Electron photonIso missing for R=%s" % R

    def chargedAllIso(self,R=0.4):
        if   R == 0.3: return self.physObj.pfIsolationVariables().sumChargedParticlePt 
        raise RuntimeError, "Electron chargedAllIso missing for R=%s" % R

    def puChargedHadronIso(self,R=0.4):
        if   R == 0.3: return self.physObj.pfIsolationVariables().sumPUPt 
        elif R == 0.4: return self.physObj.puChargedHadronIso()
        raise RuntimeError, "Electron chargedHadronIso missing for R=%s" % R




    def chargedAllIso(self):
        '''This function is used in the isolation, see Lepton class.
        Here, we replace the all charged isolation by the all charged isolation with cone veto'''
        return self.chargedAllIsoWithConeVeto()


    def dxy(self, vertex=None):
        '''Returns dxy.
        Computed using vertex (or self.associatedVertex if vertex not specified),
        and the gsf track.
        '''
        if vertex is None:
            vertex = self.associatedVertex
        return self.gsfTrack().dxy( vertex.position() )
 

    def p4(self,kind=None):
        return self.physObj.p4(self.physObj.candidateP4Kind() if kind == None else kind)

    def dz(self, vertex=None):
        '''Returns dz.
        Computed using vertex (or self.associatedVertex if vertex not specified),
        and the gsf track.
        '''
        if vertex is None:
            vertex = self.associatedVertex
        return self.gsfTrack().dz( vertex.position() )

