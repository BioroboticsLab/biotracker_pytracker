import biotracker


def track(frame, M):
    print("track " + str(frame) + str(M.shape))


def paint(qpainter, frame):
    print("paint " + str(frame))
    qpainter.setPen((255, 0, 0, 255))
    qpainter.drawRect((20, 20, 60, 60))


def shutdown():
    print("shutdown")

biotracker.run_client(track, paint, shutdown)
