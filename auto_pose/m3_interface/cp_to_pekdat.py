import os
import shutil
from auto_pose.ae import utils as u
import argparse
import glob2

workspace_path = os.environ.get('AE_WORKSPACE_PATH')

if workspace_path == None:
    print 'Please define a workspace path:\n'
    print 'export AE_WORKSPACE_PATH=/path/to/workspace\n'
    exit(-1)

parser = argparse.ArgumentParser()
parser.add_argument("experiment_group_names", nargs='+',type=str)
arguments = parser.parse_args()

pekdat_path = '/volume/pekdat/trained_models/internal/aae_models'


for i,experiment_group_names in enumerate(arguments.experiment_group_names):
    print 'copying ', experiment_group_names    
    print '%s/%s' % (i+1,len(arguments.experiment_group_names))

    full_name = experiment_group_names.split('/')
    if len(full_name) > 0:
        experiment_name = full_name.pop()
        experiment_group = full_name.pop()

        log_dir = u.get_log_dir(workspace_path,experiment_name,experiment_group)
        all_log_dirs = glob2.glob(log_dir)

        for j,log_d in enumerate(all_log_dirs):
            print 'copying ', log_d    
            print '%s/%s' % (j+1,len(all_log_dirs))

            experiment_name = os.path.basename(log_d)
            ckpt_dir = u.get_checkpoint_dir(log_d)
            train_cfg_file_path = u.get_train_config_exp_file_path(log_d, experiment_name)

            target_path = os.path.join(pekdat_path,experiment_group,experiment_name)
            target_ckpt_path = os.path.join(target_path,'checkpoints')
            if not os.path.exists(target_ckpt_path):
                os.makedirs(target_ckpt_path)

            all_ckpt_files = glob2.glob(os.path.join(ckpt_dir,'chkpt*.index'))
            base_ckpt_files = [os.path.basename(file) for file in all_ckpt_files]
            base_ckpt_files = sorted(base_ckpt_files, key=lambda x: int(x.split('-')[1].split('.')[0]))

            try:
                shutil.copy(os.path.join(ckpt_dir,'checkpoint'),target_ckpt_path)
                shutil.copy(os.path.join(ckpt_dir,base_ckpt_files[-1]),target_ckpt_path)
                shutil.copy(os.path.join(ckpt_dir,base_ckpt_files[-1].replace('.index','.meta')),target_ckpt_path)
                shutil.copy(os.path.join(ckpt_dir,base_ckpt_files[-1].replace('.index','.data-00000-of-00001')),target_ckpt_path)
                shutil.copy(train_cfg_file_path,target_path)
            except:
                print 'not copied: ',train_cfg_file_path
    else:
        print 'need experiment_group/experiment_name as arguments'
        print 'you can use regex like obj*'
    
    # gt_bb = arguments.gt_bb


