import pyrogue as pr
import pyrogue.utilities.prbs
import ldmx_ts_data

class DataRoot(pr.Root):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a ZMQ server to publish the tree
        self.zmqServer = pyrogue.interfaces.ZmqServer(root=self, addr='127.0.0.1', port=0)
        self.addInterface(self.zmqServer)

        # Instantiate the frame generator
        self.add(pyrogue.utilities.prbs.PrbsTx())

        # Instantiate the data receiver
        self.add(ldmx_ts_data.TsDaqDataReceiver())

        # Instantiate the RunControl
        self.add(pr.RunControl(
            cmd = self.PrbsTx.genFrame,
            rates = {
                0.1: '0.1 Hz',
                1: '1 Hz',
                10: '10 Hz',
                100: '100 Hz',
                1000: '1000 Hz'}))

        # Connect the PRBS stream to the data receiver
        self.PrbsTx >> self.TsDaqDataReceiver
