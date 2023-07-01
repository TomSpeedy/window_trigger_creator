# This Python file uses the following encoding: utf-8
from skl2onnx import update_registered_converter
from skl2onnx.algebra.onnx_ops import OnnxMatMul, OnnxSub
from skl2onnx.common.data_types import guess_numpy_type
def lvqModelShape(operator):
    op = operator.raw_operator
    input_type = operator.inputs[0].type.__class__
    # The shape may be unknown. *get_first_dimension*
    # returns the appropriate value, None in most cases
    # meaning the transformer can process any batch of observations.
    input_dim = operator.inputs[0].get_first_dimension()
    output_type = input_type([input_dim, 1])
    operator.outputs[0].type = output_type

def lvqModelConverter(scope, operator, container):
    op = operator.raw_operator
    opv = container.target_opset
    out = operator.outputs

    # We retrieve the unique input.
    X = operator.inputs[0]

    # In most case, computation happen in floats.
    # But it might be with double. ONNX is very strict
    # about types, every constant should have the same
    # type as the input.
    dtype = guess_numpy_type(X.type)

    # We tell in ONNX language how to compute the unique output.
    # op_version=opv tells which opset is requested
    Y = OnnxMatMul(
        OnnxSub(X, op.mean_.astype(dtype), op_version=opv),
        op.coef_.astype(dtype),
        op_version=opv, output_names=out[:1])
    Y.add_to(scope, container)
