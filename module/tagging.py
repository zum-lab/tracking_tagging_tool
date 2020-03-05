import json
import os
import random
import cv2
import numpy as np

class Tagging():
    """
    Significant Methods
        set_next_info(..)
            set serveral index of next or prev data for using get_data(..)
        set_info(..)
            set serveral index of data with information for using get_data(..)
        get_data(..)
            get current detections data
        save_detections(..)
            save new detections to json file
        show_result(..)
            show images of specific tid in every frames

    Variables
        tid_color -> dictionary
            for deciding color using tid
        tid_types -> dictionary
            for get tid in each tid type
        json_filename -> string
            for information of current data
        vidx, fidx, current -> int
            for information of current data
    """
    tid_color = {}
    tid_types = {"person":[], "vehicle":[], "bycicle":[], "motorcycle":[]}

    json_filename = ""
    vidx = -1
    fidx = -1
    current = 0

    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.json_folder_name = folder_name + "json/"
        self.img_folder_name = folder_name + "images/"

        self.filenames = [i for i in os.listdir(self.json_folder_name) if ".json" in i]
        self.filenames.sort()

    def get_all_json_filenames(self):
        """
        get all json file names when folder name is fixed
        
        return self.filenames
            self.filenames -> list
        """
        return self.filenames
    
    def get_all_vidx(self):
        """
        get all vidx when json file is fixed
        
        return all_vidx
            all_vidx -> list
        """
        all_vidx = list(set([i["video_idx"] for i in self.json_data]))
        all_vidx.sort()
        return all_vidx
    
    def get_all_fidx(self):
        """
        get all fidx when json file and vidx is fixed
        
        return all_fidx
            all_fidx -> list
        """
        all_fidx = list(set([i["frame_idx"] for i in self.json_data if i["video_idx"] == self.vidx]))
        all_fidx.sort()
        return all_fidx
    
    def get_all_tid(self):
        """
        get all tid when vidx is fixed

        return all_tid
            all_tid -> list
        """
        all_detections = [j for i in self.json_data if i["video_idx"] == self.vidx for j in i["detections"]]
        all_tid = list(set([i[5] for i in all_detections]))
        all_tid.sort()

        return all_tid

    def set_all_tid_types(self):
        """
        set self.tid_types when vidx is fixed
        """
        # init self.tid_types
        self.tid_types = {"person":[], "vehicle":[], "bycicle":[], "motorcycle":[]}

        # find all tid in self.json_data
        all_detections = [j for i in self.json_data if i["video_idx"] == self.vidx for j in i["detections"]]
        all_tid = list(set([i[5] for i in all_detections]))
        all_tid.sort(key=lambda x: int(x.split("_")[-1]))
        
        # append tid to self.tid_types
        for tid in all_tid:
            tid_type = tid.split('_')[0]
            try:
                self.tid_types[tid_type].append(tid)

            except KeyError:
                self.tid_types[tid_type] = [tid]

    def set_info(self, json_filename=None, vidx=None, fidx=None):
        """
        set self.current using json_filename, vidx, fidx
        if all is none:
            all should be first item
        if only json_filename:
            vidx and fidx should be first item
        if only jsond_filename and vidx:
            fidx should be first item
        
        argument json_filename, vidx, fidx
            json_filename, vidx, fidx -> string
        return json_filename, vidx, fidx
            json_filename -> string
            vidx, fidx -> int
        """
        self.json_filename = json_filename if json_filename else self.get_all_json_filenames()[0]
        with open(self.json_folder_name + self.json_filename) as json_file:
            self.json_data = json.load(json_file)
        
        all_vidx = self.get_all_vidx()
        new_vidx = int(vidx) if vidx else all_vidx[0]
        
        if(self.vidx is not new_vidx):
            # if vidx is changed -> init self.tid_color, self.tid_types
            self.tid_color = {}
            self.vidx = new_vidx
            
            self.set_all_tid_types()
        
        all_fidx = self.get_all_fidx()
        new_fidx = int(fidx) if fidx else all_fidx[0]
        self.fidx = new_fidx

        # search current(index of json data) with vidx and fdix
        self.current, _ = next(([index, item] for (index, item) in enumerate(self.json_data) if item["video_idx"] == self.vidx and item["frame_idx"] == self.fidx), None)
        
        return self.json_filename, self.vidx, self.fidx

    def set_next_info(self, isnext=None):
        """
        set self.current to next index of json data
        set self.vidx and self.fidx to self.current item's
        
        argument isnext
            isnext -> int(1(next) or -1(prev))
        return json_filename, vidx, fidx for redirect url
            json_filename -> string
            vidx, fidx -> int
        """
        self.current += isnext

        if(self.current >= len(self.json_data)):
            # if self.current is out of index -> self.current is 0
            self.current = 0

        new_vidx = self.json_data[self.current]["video_idx"]

        if(self.vidx is not new_vidx):
            # if vidx is changed -> init self.tid_color, self.tid_types
            self.tid_color = {}
            self.vidx = new_vidx
            
            self.set_all_tid_types()

        self.fidx = self.json_data[self.current]["frame_idx"]

        return self.json_filename, self.vidx, self.fidx

    def get_color_using_tid(self, detection):
        """
        decide color using tid randomly
        same tid should have same color -> manage using dictionary

        argument detection
            detection -> [x1, y1, x2, y2, score, tid]
        return color
            color -> [R, G, B]
        """
        tid = detection[5]
        
        try:
            # if tid key is already existed in self.tid_color
            color = self.tid_color[str(tid)]
        
        except KeyError:
            # if tid key is not in self.tid_color (KeyError)
            color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
            self.tid_color[str(tid)] = color
        
        return color

    def extract_data_from_json(self, data):
        """
        extract data from json format data

        argument data
            data -> dictionary
        return image_path, processed_detections
            image_path -> string
            processed_detections -> [[x1, y1, x2, y2, score, tid, color], ... ]
        """
        processed_detections = []
        for detection in data["detections"]:
            color = self.get_color_using_tid(detection)
            processed_detections.append(detection + [color])
        processed_detections.sort(key=lambda processed_detections: processed_detections[5])

        # this line should be modified when the data["frame_path"] format is changed
        image_path = self.img_folder_name + "/".join(data["frame_path"].split("/")[-2:])

        return image_path, processed_detections

    def get_data(self):
        """
        get processed data of self.current
        the processed data should be not object of self.json_data
        get data(image, detections) of self.current - 1 for visualization

        return current, json_filename, vidx, fidx, self.tid_types, error_message, image_path, processed_detections, pre_processed_detections, pre_image_path for visualization
            current, vidx, fidx -> int
            json_filename, image_path, pre_image_path, error_message -> string
            self.tid_types -> dictionary
            processed_detections, pre_processed_detections -> [[x1, y1, x2, y2, score, tid, color], ... ]
        """
        data = self.json_data[self.current]
        pre_data = self.json_data[self.current-1] if self.current != 0 else []
        
        pre_image_path, pre_processed_detections = self.extract_data_from_json(pre_data) if pre_data else ['None', []]
        
        image_path, processed_detections = self.extract_data_from_json(data)
        error_message = "" if os.path.isfile(image_path) else "image file does not exist"

        return [self.current, self.json_filename, self.vidx, self.fidx, self.tid_types, error_message], [image_path, processed_detections], [pre_image_path, pre_processed_detections]

    def cal_new_tidx(self, new_detection):
        """
        if new detection cal next index of tid
        update self.tid_types

        argument new_detection
            new_detections -> [x1, y1, x2, y2, score, tid, color]
        return new_detection[:6]
            new_detections -> [x1, y1, x2, y2, score, tid]
        """
        if('new' in new_detection[5]):
            # if new detection
            
            # get next tid in self.tid_types
            tid_type, _ = new_detection[5].split('_')

            try:
                next_idx = int(self.tid_types[tid_type][-1].split("_")[-1]) + 1
            except:
                next_idx = 0

            new_tid = tid_type + "_" + str(next_idx)
            
            self.tid_types[tid_type].append(new_tid)
            new_detection[5] = new_tid
            
            return new_detection[:6]
        else:
            return new_detection[:6]

    def save_detections(self, new_detections):
        """
        save modified, added, deleted new_detections to self.json_data[self.current]["detections"]
        but shape of json_file["detections"] should be not changed ([[x1, y1, x2, y2, score, tid], ... ])

        argument new_detections
            new_detections -> [[x1, y1, x2, y2, score, tid, color], ... ]
        return json_filename, vidx, fidx for redirect url
            json_filename -> string
            vidx, fidx -> int
        """
        new_detections = [self.cal_new_tidx(detection) for detection in new_detections]

        self.json_data[self.current]["detections"] = [detection[:6] for detection in new_detections]
        with open(self.json_folder_name + self.json_filename, "w") as json_file:
            json.dump(self.json_data, json_file)
        
        self.set_all_tid_types()

        return self.json_filename, self.vidx, self.fidx
    
    def get_image_path(self, directory_path, detection, frame_idx, frame_path):
        """
        save image of tid in frame and return the saved image path
        
        argument directory_path, detection, data
            directory_path -> string
            detection -> [x1, y1, x2, y2, score, tid, color]
            frame_idx -> int
            frame_path -> string
        return image_path
            image_path -> string
        """
        startX = int(detection[0])
        startY = int(detection[1])
        endX = int(detection[2])
        endY = int(detection[3])
        
        image_path = directory_path + str(frame_idx).zfill(5) + ".jpg"

        try:
            cv2.imwrite(
                image_path,
                cv2.imread(self.img_folder_name + "/".join(frame_path.split("/")[-2:]))[startY:endY, startX:endX]
            )
        except:
            cv2.imwrite(
                image_path,
                np.zeros(shape=[100, 100, 3], dtype=np.uint8)
            )

        return image_path

    def show_results(self, json_filename=None, vidx=None, tid=None):
        """
        show images of specific tid in every frames of specific json file and vidx

        argument json_filename, vidx, tid
            json_filename -> string
            vidx, tid -> int
        return [all_json, all_vidx, all_tid], [self.json_filename, self.vidx, tid], image_path_list, error_message
            all_json, all_vidx, all_tid -> list
            self.json_filename -> string
            self.vidx, tid -> int
            image_path_list -> list
            error_message -> string
        """
        error_message = ""

        all_json = self.get_all_json_filenames()
        self.json_filename = json_filename if json_filename else all_json[0]

        with open(self.json_folder_name + self.json_filename) as json_file:
            self.json_data = json.load(json_file)
        
        all_vidx = self.get_all_vidx()
        new_vidx = int(vidx) if vidx else all_vidx[0]

        if(self.vidx is not new_vidx):
            # if vidx is changed -> init self.tid_color, self.tid_types
            # this is for going back to the '/'
            self.tid_color = {}
            self.vidx = new_vidx
            
            self.set_all_tid_types()

        try:
            all_tid = self.get_all_tid()
            tid = tid if tid else all_tid[0]

            directory_path = self.img_folder_name + "results/" + str(self.vidx).zfill(5) + "_" + str(tid) + "/"

            if not (os.path.isdir(directory_path)):
                os.mkdir(directory_path)

            image_path_list = [(self.get_image_path(directory_path, detection, data["frame_idx"], data["frame_path"]), str(data["frame_idx"]))
                for data in self.json_data if data["video_idx"] == self.vidx
                    for detection in data["detections"]
                        if detection[5] == tid
            ]
            
        except:
            # there is not any tracking id
            image_path_list = []
            error_message = "There is no tracking id"
        
        return [all_json, all_vidx, all_tid], [self.json_filename, self.vidx, tid], image_path_list, error_message