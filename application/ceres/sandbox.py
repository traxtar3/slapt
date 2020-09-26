import pandas as pd


def mkTaskData():
    taskData = pd.DataFrame(columns=["Satellite", "Priority", "Task Type", "Voice Report", "Routing", "Stop", "Site"])
    taskData = taskData.append({"Satellite": "25544", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "BLE"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "25544", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "CAV"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "25544", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "COD"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "25544", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "CLR"}, ignore_index=True)
    # taskData = taskData.append({"Satellite": "25544", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "THL"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "25544", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "FYL"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "25544", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "EGL"}, ignore_index=True)

    taskData = taskData.append({"Satellite": "27880", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "BLE"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "27880", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "CAV"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "27880", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "COD"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "27880", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "CLR"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "27880", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "THL"}, ignore_index=True)
    # taskData = taskData.append({"Satellite": "27880", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "FYL"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "27880", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "EGL"}, ignore_index=True)

    taskData = taskData.append({"Satellite": "45589", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "BLE"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "45589", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "CAV"}, ignore_index=True)
    # taskData = taskData.append({"Satellite": "45589", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "COD"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "44861", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "CLR"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "44861", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "THL"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "44861", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "FYL"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "44861", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "EGL"}, ignore_index=True)

    taskData = taskData.append({"Satellite": "43931", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "BLE"}, ignore_index=True)
    # taskData = taskData.append({"Satellite": "26846", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "CAV"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "43931", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "COD"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "26846", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "CLR"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "43931", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "THL"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "26846", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "FYL"}, ignore_index=True)
    taskData = taskData.append({"Satellite": "43931", "Priority": "3D", "Task Type": "PosNeg", "Voice Report": "none", "Routing": "routine", "Stop": "UFN", "Site": "EGL"}, ignore_index=True)

    return taskData


