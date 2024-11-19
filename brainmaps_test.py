import numpy as np

from brainmaps_api_fcn.equivalence_requests import EquivalenceRequests
from brainmaps_api_fcn.subvolume_requests import SubvolumeRequest


sa = r"\\tungsten-nas.fmi.ch\tungsten\scratch\gfriedri\montruth\Reconstruction\fmi-friedrich-4dd3f21e665d.json"
volume_id = r"280984173682:montano_rm2_ngff:raw_230701_seg_240316fb"
stack_change = "240705d_rsg9_spl"
#TODO: Read list/csv
centroids_xyz = np.array([[10656, 10878, 1463], [10384, 10242, 1348], [10837, 10333, 1251], [11177, 10700, 724], [10566, 14567, 1828], [10817, 10322, 1268],
                          [11615, 13345, 1800],[11189, 12162, 2454],[11483, 12210, 2088]])


# Get the agglomerated ID that contains EM centroid
def get_agglo_group_from_point(sa, volume_id, stack_change, centroid_xyz):
    sr = SubvolumeRequest(sa, volume_id)
    vol = sr.get_subvolume(centroid_xyz, size= [1,1,1], change_stack_id = stack_change)
    agglo_id  = int(np.unique(vol[vol>0]))
    print(f"ID found: {agglo_id}")

    er = EquivalenceRequests(sa, volume_id, stack_change)
    group = er.get_groups(agglo_id)
    return group



# Create dictionary of groups
groups_dict = {}
for point in centroids_xyz:
    group = get_agglo_group_from_point(sa, volume_id, stack_change, point)
    groups_dict[tuple(point)] = group


for key, value in groups_dict.items():
    print(key)
    print(value)



#
#
# # Extract bbox from segments
# from google.cloud import bigquery
#
#
# # Initialize the client
# client = bigquery.Client(project='fmi-friedrich')  # specify your project ID
#
# # Your query to find objects containing a specific point
# query = """
# SELECT id, bbox
# FROM `fmi-friedrich.ruth_ob.raw_230701_seg_240316fb_240705d_rsg9_spl_objinfo`
# WHERE
#     bbox.start.z <= 11481 AND (bbox.start.z + bbox.size.z) >= 11481 AND
#     bbox.start.y <= 12141 AND (bbox.start.y + bbox.size.y) >= 12141 AND
#     bbox.start.x <= 2303 AND (bbox.start.x + bbox.size.x) >= 2303
# ORDER BY
#     POW(center_of_mass.x - 2303, 2) +
#     POW(center_of_mass.y - 12141, 2) +
#     POW(center_of_mass.z - 11481, 2)
# LIMIT 1
# """
#
# # Execute the query
# query_job = client.query(query)
# results = query_job.result()
#
# # Print results
# for row in results:
#     print(f"ID: {row.id}")
#     print(f"Bbox start: x={row.bbox.start.x}, y={row.bbox.start.y}, z={row.bbox.start.z}")
#     print(f"Bbox size: x={row.bbox.size.x}, y={row.bbox.size.y}, z={row.bbox.size.z}")

# Create convex hulls

# Create overlap matrix
