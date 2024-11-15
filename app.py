from flask import Flask, render_template, Response, send_file, redirect, url_for
import cv2
import os

app = Flask(__name__)
camera = None  # Initialize camera as None

@app.route('/')
def index():
    # Main page with two buttons: Start Stream and View Stream
    return render_template('index.html')

@app.route('/start_stream')
def start_stream():
    global camera
    # Start the stream by opening the camera if it's not already open
    if camera is None or not camera.isOpened():
        camera = cv2.VideoCapture(0)
    return redirect(url_for('view_stream'))

@app.route('/view_stream')
def view_stream():
    # Render the view stream page
    return render_template('view_stream.html')

def gen_frames():
    global camera
    while True:
        if camera and camera.isOpened():
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break

@app.route('/video_feed')
def video_feed():
    # Video streaming route for display in the HTML img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture():
    global camera
    success, frame = camera.read() if camera and camera.isOpened() else (False, None)
    if success:
        # Ensure the 'static' directory exists
        img_dir = 'static'
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        
        img_path = os.path.join(img_dir, 'capture.jpg')
        cv2.imwrite(img_path, frame)
        return send_file(img_path, as_attachment=True)
    return "Failed to capture image", 500

@app.route('/stop_stream')
def stop_stream():
    global camera
    # Release the camera resource when done
    if camera and camera.isOpened():
        camera.release()
        camera = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)