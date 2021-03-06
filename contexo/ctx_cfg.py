###############################################################################
#                                                                             #
#   ctx_cfg.py                                                                #
#   Component of Contexo Shell - (c) Scalado AB 2008                          #
#                                                                             #
#   Author: Manuel Astudillo (manuel.astudillo@scalado.com)                   #
#                                                                             #
#   ------------                                                              #
#                                                                             #
###############################################################################

from config import Config
import os.path
import shutil

#------------------------------------------------------------------------------
def expanduser_path_list( path_list ):
    exp_path_list = list()
    if type(path_list) != list:
        path_list = [path_list,]

    for path in path_list:
        exp_path_list.append( os.path.expanduser( path ) )

    return exp_path_list


#------------------------------------------------------------------------------
class CFGFile:
#TODO: maybe add has_key function. Or are all keys obligatory now?
    def __init__( self, cfgFilePath = None ):
        self.path            = cfgFilePath
        self.defaultBConf    = str()
        self.defaultView     = str()
        self.bcPaths         = list()
        self.cdefPaths       = list()
        self.EnvPaths        = list()
        self.verboseLevel    = 1

        #Copy default config into the user's directory if needed
        if not os.path.exists(cfgFilePath):
            import ctx_common
            defconfig = os.path.join( os.path.dirname(__file__), os.path.normpath('defaults/contexo.cfg')  )
            ctx_common.infoMessage("Copying config from '%s' to '%s'"%(defconfig,  cfgFilePath),  1)
            try:
                shutil.copy( defconfig,  cfgFilePath )
            except IOError, (errno, strerror):
                print "*** Error copying file %s"%defconfig
                print strerror
                raise IOError

        self.cfgFile = Config( cfgFilePath )

    def saveAs ( self, filePath ):
        #TODO: Shouldn't filePath be stored in self.path?
        self.cfgFile.save ( filePath )

    def update ( self ):
        self.saveAs ( self.path )

    def getDefaultBConf ( self ):
        return self.cfgFile.get_item ('default', 'CTX_DEFAULT_BCONF')

    # Deprecated.
    #def getDefaultView ( self ):
    #    self.cfgFile.get_item ('default', 'CTX_DEFAULT_VIEW')

    # Deprecated
    #def setDefaultView ( self, viewFile ):
    #    self.cfgFile.add_item ('default', 'CTX_DEFAULT_VIEW', viewFile )

    def getBConfPaths ( self ):
        return expanduser_path_list( self.cfgFile.get_item('default', 'CTX_BCONF_PATHS') )

    def getCDefPaths ( self ):
        return expanduser_path_list( self.cfgFile.get_item ('default', 'CTX_CDEF_PATHS') )

    def getEnvPaths ( self ):
        return expanduser_path_list( self.cfgFile.get_item ('default', 'CTX_ENV_PATHS') )

    def getVerboseLevel ( self ):
        return self.cfgFile.get_item ('default', 'CTX_VERBOSE_LEVEL')

    def setDefaultBConf ( self, bconfFile ):
        self.cfgFile.add_item ('default', 'CTX_DEFAULT_BCONF', bconfFile )

    def setBConfPaths ( self, bconfPaths ):
        self.cfgFile.add_item ('default', 'CTX_BCONF_PATHS', bconfPaths)

    def setCDefPaths ( self, cdefPaths ):
        self.cfgFile.add_item ('default', 'CTX_CDEF_PATHS', cdefPaths )

    def setEnvPaths ( self, envPaths ):
        self.cfgFile.add_item ('default', 'CTX_ENV_PATHS', envPaths )

    def setVerboseLevel ( self, verboseLevel ):
        self.cfgFile.add_item ('default', 'CTX_VERBOSE_LEVEL', verboseLevel )
