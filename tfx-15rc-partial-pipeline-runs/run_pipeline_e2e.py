"""
MNIST Pipeline
"""

from absl import app, flags, logging
from tfx import components
from tfx.orchestration import pipeline
from tfx.orchestration.local.local_dag_runner import LocalDagRunner

FLAGS = flags.FLAGS
flags.DEFINE_string("pipeline_name", "mnist_pipeline", help="name of this pipeline")
flags.DEFINE_string("pipeline_root", "./pipeline_root", help="root directory fot this pipeline")
flags.DEFINE_string("mnist_base_path", "gs://tfds-data/datasets/mnist/3.0.1", help="name of this pipeline")


def main(_):
    LocalDagRunner().run(_create_pipeline())


def _create_pipeline() -> pipeline.Pipeline:
    logging.info(f"Pipeline name: {FLAGS.pipeline_name}")
    logging.info(f"input_base for MNIST data: {FLAGS.mnist_base_path}")

    example_gen = components.ImportExampleGen(input_base=FLAGS.mnist_base_path)

    return pipeline.Pipeline(
        pipeline_name=FLAGS.pipeline_name,
        pipeline_root=FLAGS.pipeline_root,
        components=[
            example_gen
        ],
    )


if __name__ == "__main__":
    app.run(main)
