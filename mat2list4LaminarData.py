import numpy as np
import matplotlib.pyplot as plt

class EEG4Laminar:
    def __init__(self,data):
        self.csd_info = None
        self.srate_info = None
        self.timevec_info = None
        self.csddata = None
        self.times = None

        self.set_info(data)
        self.set_data(data)

    def set_info(self,data):
        self.csd_info = data["csd"].shape
        self.srate_info = data["srate"].shape
        self.timevec_info = data["timevec"].shape
    
    def set_data(self,data):
        self.csddata = data["csd"]
        self.timevec = data["timevec"]

    def erp_plot(self,chan2plot):

        erp_data = np.mean(self.csddata, axis=2)

        plt.figure(figsize=(15,3))
        plt.plot(self.timevec.T, erp_data[chan2plot,:])
        plt.xlim([-0.1,1.3])
        plt.ylim([-500,1000])
        plt.title(f"ERP from channel {chan2plot+1}")
        plt.ylabel("Voltage ($\mu$V)")
        plt.show()
    
    def imagesc(self, chan2plot):
        data2plot = self.csddata[chan2plot,:,:]
        plt.imshow(data2plot.T, aspect='auto', vmin=0, vmax=1000,
                origin='upper')
        plt.xlabel("Time")
        plt.ylabel("Trials")
        plt.show()
    
    def contourf(self):
        data2plot = np.mean(self.csddata, axis=2)
        plt.imshow(data2plot, aspect='auto', vmin=0, vmax=100,
                origin='upper')
        plt.xlabel("Time")
        plt.ylabel("Channel")
        plt.show()