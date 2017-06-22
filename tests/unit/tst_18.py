from __future__ import division
import iotbx.pdb
import os
from scitbx.array_family import flex
from libtbx import easy_pickle
import time
import run_tests
from libtbx.test_utils import approx_equal
import libtbx.load_env

qrefine = libtbx.env.find_in_repositories("qrefine")
qr_unit_tests_data = os.path.join(qrefine,"tests","unit","data_files")

def run(prefix = "tst_18"):
  """
  Exercise gradients match:
    - one conformer in buffer region vs two conformers in buffer region
      -- using clustering with less clusters vs not using clustering.
      -- using clustering with more clusters vs not using clustering.
  """
  for data_file_prefix in ["h_altconf", "h_altconf_2"]:
    for maxnum in ["15", "2"]:
      common_args = ["restraints=cctbx", "mode=opt", "nproc=1"] +\
                    ["maxnum_residues_in_cluster="+maxnum]
      r = run_tests.run_cmd(prefix,
        args     = common_args+["clustering=true",
                                "dump_gradients=cluster_true.pkl"],
        pdb_name = os.path.join(qr_unit_tests_data,"%s.pdb"%data_file_prefix),
        mtz_name = os.path.join(qr_unit_tests_data,"%s.mtz"%data_file_prefix))
      r = run_tests.run_cmd(prefix,
        args     = common_args+["clustering=false",
                               "dump_gradients=cluster_false.pkl"],
        pdb_name = os.path.join(qr_unit_tests_data,"%s.pdb"%data_file_prefix),
        mtz_name = os.path.join(qr_unit_tests_data,"%s.mtz"%data_file_prefix))
      #
      g1 = flex.vec3_double(easy_pickle.load("cluster_false.pkl"))
      g2 = flex.vec3_double(easy_pickle.load("cluster_true.pkl"))
      assert g1.size() == g2.size()
      diff = g1-g2
      if(0):
        for i, diff_i in enumerate(diff):
          print i, diff_i#, g1[i], g2[i]
      assert approx_equal(diff.max(), [0,0,0])

if __name__ == '__main__':
  t0 = time.time()
  prefix = "tst_18"
  if(1):
    run(prefix)
    print prefix + ":  OK  " + "Time: %6.2f (s)" % (time.time() - t0)
  else:
    print prefix + ":  Skipped    "
