import biotracker

Mat = None


def track(frame, M):
    global Mat
    Mat = M
    print("track " + str(frame) + str(M.shape))


def paint(qpainter, frame):
    global Mat
    print("paint " + str(frame))
    qpainter.setPen((255, 0, 0, 255))
    qpainter.drawRect((20, 20, 60, 60))
    if Mat is not None:
        return Mat



def shutdown():
    print("shutdown")

biotracker.run_client(track, paint, shutdown)
