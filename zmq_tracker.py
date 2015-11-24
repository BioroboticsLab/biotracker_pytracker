import biotracker


def track(frame, M):
    print("track " + str(frame))


def paint(frame):
    print("paint " + str(frame))


def shutdown():
    print("shutdown")

biotracker.run_client(track, paint, shutdown)
