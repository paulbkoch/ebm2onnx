import os
import tempfile
import pytest

import numpy as np
import onnx
import onnxruntime as rt
import ebm2onnx.graph as graph


def infer_model(model, input):
    _, filename = tempfile.mkstemp()
    try:
        onnx.save_model(model, filename)
        sess = rt.InferenceSession(filename)
        for o in sess.get_outputs():
            print(o)
        pred = sess.run(None, input)

        return pred

    finally:
        os.unlink(filename)


def assert_model_result(g, input, expected_result, atol=1e-08):
    model = graph.compile(g)
    _, filename = tempfile.mkstemp()
    try:
        onnx.save_model(model, filename)
        sess = rt.InferenceSession(filename)
        pred = sess.run(None, input)

        print(pred)
        for i, p in enumerate(pred):
            assert np.allclose(p, np.array(expected_result[i]))

    finally:
        os.unlink(filename)
