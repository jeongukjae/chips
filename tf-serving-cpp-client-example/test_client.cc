#include "grpcpp/grpcpp.h"
#include "tensorflow_serving/apis/prediction_service.grpc.pb.h"

#define HOST "0.0.0.0:8500"
#define MODEL_NAME "half_plus_two"
#define MODEL_SIGNATURE_NAME "serving_default"

int main() {
  tensorflow::serving::PredictRequest predictRequest;
  tensorflow::serving::PredictResponse predictResponse;
  grpc::ClientContext clientContext;

  predictRequest.mutable_model_spec()->set_name(MODEL_NAME);
  predictRequest.mutable_model_spec()->set_signature_name(MODEL_SIGNATURE_NAME);
  auto inputMap = predictRequest.mutable_inputs();

  tensorflow::TensorProto inputTensor;
  inputTensor.set_dtype(tensorflow::DataType::DT_FLOAT);
  inputTensor.mutable_tensor_shape()->add_dim()->set_size(1);
  inputTensor.mutable_tensor_shape()->add_dim()->set_size(3);
  inputTensor.add_float_val(1.0f);
  inputTensor.add_float_val(2.0f);
  inputTensor.add_float_val(5.0f);
  (*inputMap)["x"] = inputTensor;

  for (const auto& inputPair : *inputMap) {
    std::cout << "Input " << inputPair.first << std::endl;
    auto tensor = inputPair.second;

    for (const auto val : tensor.float_val()) {
      std::cout << "\t" << val;
    }
    std::cout << std::endl;
  }

  std::unique_ptr<tensorflow::serving::PredictionService::Stub> stub =
      tensorflow::serving::PredictionService::NewStub(
          grpc::CreateChannel(HOST, grpc::InsecureChannelCredentials()));

  grpc::Status status =
      stub->Predict(&clientContext, predictRequest, &predictResponse);

  if (!status.ok()) {
    std::cerr << "Error code: " << status.error_code()
              << ", message: " << status.error_message() << std::endl;
    return 1;
  }

  for (const auto& outputPair : predictResponse.outputs()) {
    std::cout << "Output " << outputPair.first << std::endl;
    auto tensor = outputPair.second;

    for (const auto val : tensor.float_val()) {
      std::cout << "\t" << val;
    }
    std::cout << std::endl;
  }
}
