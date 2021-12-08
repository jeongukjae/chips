import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text  # noqa
from absl import app, flags, logging

FLAGS = flags.FLAGS
flags.DEFINE_string("encoder", "https://tfhub.dev/jeongukjae/smaller_LaBSE_15lang/1", help="url for encoder")
flags.DEFINE_string("preprocessor", "https://tfhub.dev/jeongukjae/smaller_LaBSE_15lang_preprocess/1", help="url for preprocessor")
flags.DEFINE_string("output", "models/smaller-LaBSE/1", help="path to export model")


def main(argv):
    # Loading models from tfhub.dev
    encoder = hub.KerasLayer(FLAGS.encoder)
    preprocessor = hub.KerasLayer(FLAGS.preprocessor)

    # Constructing model to encode texts into high-dimensional vectors
    sentences = tf.keras.layers.Input(shape=(), dtype=tf.string, name="sentences")
    encoder_inputs = preprocessor(sentences)
    sentence_representation = encoder(encoder_inputs)["pooled_output"]
    normalized_sentence_representation = tf.nn.l2_normalize(sentence_representation, axis=-1)  # for cosine similarity
    model = tf.keras.Model(sentences, normalized_sentence_representation)
    model.summary()

    model.save(FLAGS.output)
    logging.info("Done")


if __name__ == "__main__":
    app.run(main)
