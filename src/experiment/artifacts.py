from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from utils.files import PickleFile, TarFile
from utils.logger import logger


@dataclass
class ExperimentArtifacts:
    run_tag: str
    model_name: str
    base_path: Path

    def _create_if_not_exist(self):
        Path(self.output_prefix).mkdir(parents=True, exist_ok=True)

    @property
    def output_prefix(self):
        return self.base_path / self.model_name

    def get_artifacts(self, artifacts: Dict[str, Any]):
        self.metrics = artifacts.get("metrics")
        self.figures = artifacts.get("figures")
   
    def save_results(self):
        self._create_if_not_exist()
        if self.metrics:
            metrics_path = str(self.output_prefix / 'metrics.txt')
            with open(metrics_path, 'w') as outfile:
                for k, v in self.metrics.items():
                    outfile.write(f"{k}: {v:.3f}\n")
        if self.figures:
            for k, fig in self.figures.items():
                fig.savefig(str(self.output_prefix / f'{k}.png'))


    def save(self):
        self.save_results()

    # Create single output for Sagemaker training-job
    @property
    def model_package_path(self):
        return self.base_path / 'model.tar.gz'

    def create_package_with_models(self):
        logger.info(f"Loading models from {self.base_path}")
        model_paths = {}
        for p in sorted(self.base_path.glob("**/*joblib")):
            tar_path = f"{p.parent.name}/{p.name}"
            model_paths[str(p)] = tar_path
        TarFile.compress(self.model_package_path, model_paths)
