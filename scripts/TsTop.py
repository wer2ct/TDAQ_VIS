import pyrogue
import pyrogue.pydm
pyrogue.addLibraryPath('../python/')
import ldmx_ts_data

with ldmx_ts_data.DataRoot() as root:
    pyrogue.pydm.runPyDM(
        serverList=root.zmqServer.address,
        title='Warm TDM',
        sizeX=500,
        sizeY=500)
