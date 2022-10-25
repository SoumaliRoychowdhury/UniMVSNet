import os
from typing import Dict
from pathlib import Path
from rar_algo.utils.general.configurator import Config
from rar_algo.algo.step_interface import StepInterface
from rar_algo.algo.CasMVSNet.gipuma import probability_filter, mvsnet_to_gipuma, depth_map_fusion


class FusibileInterface(StepInterface):
    def __init__(self, step_name, step_config, working_dir: str, step_description: str=""):
        super().__init__(step_name, step_config, working_dir, step_description)

    @property
    def is_active(self) -> bool:
        return self.step_config.do_fusibile

    def define_input_artifacts(self) -> Dict:
        input_artifacts = super().define_input_artifacts()
        input_artifacts["input_folder"] = self.working_dir
        return input_artifacts
    
    def define_output_artifacts(self) -> Dict:
        output_artifacts = super().define_output_artifacts()
        return output_artifacts

    def algorithm(self):
        # probability filter
        print("Gipuma: filter depth map with probability map")
        probability_filter(self.dense_folder, self.step_config.prob_threshold)

        # convert to gipuma format
        print("Gipuma: Convert mvsnet output to gipuma input")
        mvsnet_to_gipuma(self.dense_folder, self.point_folder)

        # depth map fusion with gipuma
        print("Gipuma: Run depth map fusion & filter")
        depth_map_fusion(
            self.point_folder, self.step_config.fusibile_exe_path, 
            self.step_config.disp_threshold, self.step_config.num_consistent
        )

    def preprocessing(self):
        # check in conf class name of depth pred net
        depth_net_name = f"{Config.content.depth_net}-output"
        self.dense_folder = os.path.join(self.input_artifacts["input_folder"], depth_net_name)
        self.point_folder = os.path.join(self.dense_folder, 'points_mvsnet')
        self.step_config.fusibile_exe_path = os.path.join(
            Path(os.path.realpath(__file__)).parents[1],
            self.step_config.fusibile_exe_path
        )
        if not os.path.isdir(self.point_folder):
            os.mkdir(self.point_folder)

    def postprocessing(self):
        pass
