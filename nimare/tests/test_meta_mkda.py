"""
Test nimare.meta.mkda (KDA-based meta-analytic algorithms).
"""
import numpy as np

import nimare
from nimare.correct import FDRCorrector, FWECorrector
from nimare.meta import kernel, mkda


def test_mkda_density_kernel_instance_with_kwargs(testdata_cbma):
    """
    Smoke test for MKDADensity with a kernel transformer object, with kernel
    arguments provided, which should result in a warning, but the original
    object's parameters should remain untouched.
    """
    kern = kernel.MKDAKernel(r=2)
    meta = mkda.MKDADensity(kern, kernel__r=6, null_method="empirical", n_iters=100)

    assert meta.kernel_transformer.get_params().get("r") == 2


def test_mkda_density_kernel_class(testdata_cbma):
    """
    Smoke test for MKDADensity with a kernel transformer class.
    """
    meta = mkda.MKDADensity(kernel.MKDAKernel, kernel__r=5, null_method="empirical", n_iters=100)
    res = meta.fit(testdata_cbma)
    assert isinstance(res, nimare.results.MetaResult)


def test_mkda_density_kernel_instance(testdata_cbma):
    """
    Smoke test for MKDADensity with a kernel transformer object.
    """
    kern = kernel.MKDAKernel(r=5)
    meta = mkda.MKDADensity(kern, null_method="empirical", n_iters=100)
    res = meta.fit(testdata_cbma)
    assert isinstance(res, nimare.results.MetaResult)


def test_mkda_density_analytic_null(testdata_cbma_full):
    """
    Smoke test for MKDADensity
    """
    meta = mkda.MKDADensity(null="analytic")
    res = meta.fit(testdata_cbma_full)
    corr = FWECorrector(method="montecarlo", voxel_thresh=0.001, n_iters=1, n_cores=1)
    cres = corr.transform(res)
    assert isinstance(res, nimare.results.MetaResult)
    assert isinstance(cres, nimare.results.MetaResult)


def test_mkda_density(testdata_cbma):
    """
    Smoke test for MKDADensity
    """
    meta = mkda.MKDADensity(null_method="empirical", n_iters=100)
    res = meta.fit(testdata_cbma)
    corr = FWECorrector(method="montecarlo", voxel_thresh=0.001, n_iters=5, n_cores=1)
    cres = corr.transform(res)
    assert isinstance(res, nimare.results.MetaResult)
    assert isinstance(cres, nimare.results.MetaResult)


def test_mkda_chi2_fdr(testdata_cbma):
    """
    Smoke test for MKDAChi2
    """
    meta = mkda.MKDAChi2()
    res = meta.fit(testdata_cbma, testdata_cbma)
    corr = FDRCorrector(method="bh", alpha=0.001)
    cres = corr.transform(res)
    assert isinstance(res, nimare.results.MetaResult)
    assert isinstance(cres, nimare.results.MetaResult)


def test_mkda_chi2_fwe_1core(testdata_cbma):
    """
    Smoke test for MKDAChi2
    """
    meta = mkda.MKDAChi2()
    res = meta.fit(testdata_cbma, testdata_cbma)
    corr = FWECorrector(method="montecarlo", n_iters=5, n_cores=1)
    cres = corr.transform(res)
    assert isinstance(res, nimare.results.MetaResult)
    assert isinstance(cres, nimare.results.MetaResult)


def test_mkda_chi2_fwe_2core(testdata_cbma):
    """
    Smoke test for MKDAChi2
    """
    meta = mkda.MKDAChi2()
    res = meta.fit(testdata_cbma, testdata_cbma)
    assert isinstance(res, nimare.results.MetaResult)
    corr_2core = FWECorrector(method="montecarlo", n_iters=5, n_cores=2)
    cres_2core = corr_2core.transform(res)
    assert isinstance(cres_2core, nimare.results.MetaResult)


def test_kda_density_fwe_1core(testdata_cbma):
    """
    Smoke test for KDA with empirical null and FWE correction.
    """
    meta = mkda.KDA(null_method="empirical", n_iters=100)
    res = meta.fit(testdata_cbma)
    corr = FWECorrector(method="montecarlo", n_iters=5, n_cores=1)
    cres = corr.transform(res)
    assert isinstance(res, nimare.results.MetaResult)
    assert res.get_map("p", return_type="array").dtype == np.float64
    assert isinstance(cres, nimare.results.MetaResult)
    assert (
        cres.get_map("logp_level-voxel_corr-FWE_method-montecarlo", return_type="array").dtype
        == np.float64
    )
