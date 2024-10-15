import numpy as np
import matplotlib.pyplot as plt

import mne

attributes = [
    "setname",
    "filename",
    "filepath",
    "subject",
    "group",
    "condition",
    "session",
    "comments",
    "nbchan",
    "trials",
    "pnts",
    "srate",
    "xmin",
    "xmax",
    "times",
    "data",
    "icaact",
    "icawinv",
    "icasphere",
    "icaweights",
    "icachansind",
    "chanlocs",
    "urchanlocs",
    "chaninfo",
    "ref",
    "event",
    "urevent",
    "eventdescription",
    "epoch",
    "epochdescription",
    "reject",
    "stats",
    "specdata",
    "specicaact",
    "splinefile",
    "icasplinefile",
    "dipfit",
    "history",
    "saved",
    "etc",
    "spedata"
]

shape_attributes = [
    "times",
    "data",
    "chanlocs",
    "chaninfo",
    "event",
    "urevent",
    "epoch",
    "reject",
    "stats",
    "etc"
]

chan_infos = [
    "labels",
    "theta",
    "radius",
    "X",
    "Y",
    "Z",
    "sph_theta",
    "sph_phi",
    "sph_radius",
    "type",
    "urchan"
]

epoch_infos = [
    "event",
    "eventduration",
    "eventlatency", ## eventin gerçekleşme zamanları
    "eventtype",
    "eventurevent"
]

class EEG:
    def __init__(self,data):
        for attribute in attributes:
            setattr(self, attribute, None)
        for chan_info in chan_infos:
            setattr(self, chan_info, None)
        for epoch_info in epoch_infos:
            setattr(self, epoch_info, None)

        self.eegdata = data["EEG"][0][0]["data"]
        self.eegtimes = data["EEG"][0][0]["times"]

        self.set_info(data)
        self.set_chanlocs(data)
        self.set_epochs(data)
    
    def set_info(self,data):
        for attribute in attributes:
            try:
                if attribute in shape_attributes:
                    setattr(self, attribute, data["EEG"][attribute][0][0].shape)
                elif attribute == "ref":
                    setattr(self, attribute, data["EEG"][attribute][0][0][0].tolist())
                else:
                    setattr(self, attribute, data["EEG"][attribute][0][0].item())
            except ValueError:
                pass

    def set_chanlocs(self,data):
        for chan_info in chan_infos:
            chan_values = []
            for chan in range(self.chanlocs[1]):
                try:    
                    chan_values.append(data["EEG"]["chanlocs"][0][0][chan_info][0][chan].item())
                except ValueError:
                    chan_values.append([])
                setattr(self, chan_info, chan_values)

    def set_epochs(self,data):
        event_list = []
        eventduration_list = []
        eventlatency_list = []
        eventtype_list =[]
        eventurevent_list = []

        for i in range(self.epoch[1]):
            event_list.append(data["EEG"]["epoch"][0][0][0][i][0].tolist()[0])

            temp = data["EEG"]["epoch"][0][0][0][i][1][0]
            eventValue = [value[0][0].item() for value in temp]
            eventduration_list.append(eventValue)

            temp = data["EEG"]["epoch"][0][0][0][i][2][0]
            eventValue = [value[0][0].item() for value in temp]
            eventlatency_list.append(eventValue)

            temp = data["EEG"]["epoch"][0][0][0][i][3][0]
            eventValue = [value[0][0].item() for value in temp]
            eventtype_list.append(eventValue)

            temp = data["EEG"]["epoch"][0][0][0][i][4][0]
            eventValue = [value[0][0].item() for value in temp]
            eventurevent_list.append(eventValue)

        self.event = event_list
        self.eventduration = eventduration_list
        self.eventlatency = eventlatency_list
        self.eventtype = eventtype_list
        self.eventurevent = eventurevent_list

    def erp_plot(self,chan2plot):
        erp = np.mean(self.eegdata, axis=2)
        labels_np = np.array(self.labels)
        idxChan = np.where(labels_np == chan2plot)[0]

        plt.plot(self.eegtimes[0], erp[idxChan,:][0],"k")
        plt.show()

    def topo_plot(self, idxTime):
        head_rad = 0.095
        plot_rad = 0.51
        squeezefac = head_rad / plot_rad

        eeg_chanlocs = []

        for i in range(64):
            th = self.theta[i]
            rd = self.radius[i]

            theta_rad = np.deg2rad(th)
            x = rd * np.cos(theta_rad)
            y = rd * np.sin(theta_rad)
            eeg_chanlocs.append([y*squeezefac, x*squeezefac])

        eeg_chanlocs = np.array(eeg_chanlocs)

        fig,ax = plt.subplots(figsize=(8,8))
        erp = np.mean(self.eegdata, axis=2)
        im, _ = mne.viz.plot_topomap(erp[:,idxTime], eeg_chanlocs, axes=ax, show=False, 
                                cmap="RdBu_r",ch_type="eeg", size=200, contours=6, 
                                vlim=(self.xmin*3,self.xmax*4)
                                )
        plt.colorbar(im)
        plt.title('ERP from {} ms'.format(self.eegtimes[:,idxTime]))
        plt.show()