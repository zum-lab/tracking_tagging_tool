import json
import sys

from flask import Flask, render_template, request, redirect, url_for
from module.tagging import Tagging

app = Flask(__name__)

tagging = Tagging("./static/")

@app.route('/')
def index():
    """
    /
        show first frame of first video of frist json
    /?json= &vidx= &fidx=
        show specific frame
    /?next=
        show next frame
        redirect /?json= &vidx= &fidx=
    /?is_save= &detections= 
        save new detections and reload
        redirect /?json= &vidx= &fidx=

    error
        error in set info: alert error message, show first frame of first video of frist json
        error in get data: alert error message
    """
    error_message = ""

    jsonfile = request.args.get('json')
    vidx = request.args.get('vidx')
    fidx = request.args.get('fidx')
    
    tid = request.args.get('tid')

    is_next = request.args.get('next')
    is_save = request.args.get('save')
    
    detections = request.args.get('detections')
    
    if(is_save and detections):
        # if save new detections
        # and redirect url
        detections = json.loads(detections)
        json_filename, vidx, fidx = tagging.save_detections(detections)
        return redirect(url_for('index', json=json_filename, vidx=vidx, fidx=fidx))
    
    else:
        # else (set information vidx, fidx, self.current ...)

        try:
            if(is_next):
                # set next information when next or prev button is clicked
                # and redirect url
                json_filename, vidx, fidx = tagging.set_next_info(int(is_next))
                return redirect(url_for('index', json=json_filename, vidx=vidx, fidx=fidx))
            
            else:
                # set specific information when json file is changed or search button is clicked
                json_filename, vidx, fidx = tagging.set_info(json_filename=jsonfile, vidx=vidx, fidx=fidx)
        
        except:
            # if abnormal access (e.g., when first approach is url/?next=1)
            error_message = "error: check url"
            json_filename, vidx, fidx = tagging.set_info()

    info, data, pre_data = tagging.get_data()
    """
    info -> [current, json_filename, vidx, fidx, tid_types, error_message]
    data -> [image_path, detections]
    pre_data -> [pre_image_path, pre_detections]
        current, vidx, fidx -> int
        json_filename, image_path, pre_image_path, error_message -> string
        tid_types -> dictionary
        detections, pre_detections -> [[x1, y1, x2, y2, score, tid, color], ... ]
    """

    error_message = info[5] if info[5] != "" else error_message

    # for select list of select box
    json_list = tagging.get_all_json_filenames()
    vidx_list = tagging.get_all_vidx()
    fidx_list = tagging.get_all_fidx()
    
    return render_template(
        'index.html',
        img_name=data[0], detections=data[1],
        pre_img_name=pre_data[0], pre_detections=pre_data[1],
        jsonfile=info[1], vidx=info[2], fidx=info[3], tid=tid,
        json_list=json_list, vidx_list=vidx_list, fidx_list=fidx_list,
        tid_types=info[4],
        error_message=error_message
    )

@app.route('/fin')
def fin():
    """
    /fin
        show first tid of first video of frist json
    /fin?json= &vidx= &tid=
        show specific tid in every frames
    
    error
        alert error message
    """
    error_message = ''

    jsonfile = request.args.get('json')
    vidx = request.args.get('vidx')
    tid = request.args.get('tid')
    
    [json_list, vidx_list, tid_list], [jsonfile, vidx, tid], image_path_list, error_message = tagging.show_results(json_filename=jsonfile, vidx=vidx, tid=tid)
    
    return render_template(
        'fin.html',
        image_path_list=image_path_list,
        jsonfile=jsonfile, vidx=vidx, tid=tid,
        json_list=json_list, vidx_list=vidx_list, tid_list=tid_list,
        error_message=error_message
    )