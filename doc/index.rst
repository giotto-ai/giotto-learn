.. giotto-learn documentation master file, created by
   sphinx-quickstart on Mon Jun  3 11:56:46 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to giotto's API reference!
==================================


:mod:`giotto.mapper`: Mapper
============================

.. automodule:: giotto.mapper
   :no-members:
   :no-inherited-members:

Filters
-------
.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: class.rst

   mapper.Projection
   mapper.Eccentricity
   mapper.Entropy

Covers
-------
.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: class.rst

   mapper.OneDimensionalCover
   mapper.CubicalCover

Clustering
----------
.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: class.rst

   mapper.FirstSimpleGap
   mapper.FirstHistogramGap

Pipeline
--------
.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: function.rst

   mapper.pipeline.make_mapper_pipeline


.. autosummary::
   :toctree: generated/
   :template: class.rst

   mapper.pipeline.MapperPipeline

Visualization
-------------
.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: function.rst

   mapper.visualization.plot_static_mapper_graph
   mapper.visualization.plot_interactive_mapper_graph

Utilities
---------
.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: function.rst

   mapper.utils.decorators.method_to_transform
   mapper.utils.pipeline.transformer_from_callable_on_rows


:mod:`giotto.homology`: Persistent homology
===========================================

.. automodule:: giotto.homology
   :no-members:
   :no-inherited-members:

.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: class.rst

   homology.VietorisRipsPersistence
   homology.ConsistentRescaling


:mod:`giotto.diagrams`: Persistence diagrams
============================================

.. automodule:: giotto.diagrams
   :no-members:
   :no-inherited-members:

Preprocessing
-------------
.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: class.rst

   diagrams.ForgetDimension
   diagrams.Scaler
   diagrams.Filtering

Distances
---------
.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: class.rst

   diagrams.PairwiseDistance

Diagram features
----------------
.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: class.rst

   diagrams.Amplitude
   diagrams.PersistenceEntropy
   diagrams.PersistenceLandscape
   diagrams.BettiCurve
   diagrams.HeatKernel


:mod:`giotto.time_series`: Time series
======================================

.. automodule:: giotto.time_series
   :no-members:
   :no-inherited-members:

Preprocessing
-------------
.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: class.rst

   time_series.SlidingWindow
   time_series.Resampler
   time_series.Stationarizer

Time-delay embedding
--------------------
.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: class.rst

   time_series.TakensEmbedding

Target preparation
------------------
.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: class.rst

   time_series.Labeller

Dynamical systems
-----------------
.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: class.rst

   time_series.PermutationEntropy

Multivariate
------------
.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: class.rst

   time_series.PearsonDissimilarity


:mod:`giotto.graphs`: Graphs
============================

.. automodule:: giotto.graphs
   :no-members:
   :no-inherited-members:

Graph creation
--------------
.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: class.rst

   graphs.TransitionGraph
   graphs.KNeighborsGraph

Graph processing
----------------
.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: class.rst

   graphs.GraphGeodesicDistance
   

:mod:`giotto.base`: Base
========================

.. automodule:: giotto.base
   :no-members:
   :no-inherited-members:

.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: class.rst

   base.TransformerResamplerMixin


:mod:`giotto.pipeline`: Pipeline
================================

.. automodule:: giotto.pipeline
   :no-members:
   :no-inherited-members:

.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: class.rst

   pipeline.Pipeline

.. autosummary::
   :toctree: generated/
   :template: function.rst

   pipeline.make_pipeline


:mod:`giotto.meta_transformers`: Convenience pipelines
======================================================

.. automodule:: giotto.meta_transformers
   :no-members:
   :no-inherited-members:

.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: class.rst

   meta_transformers.EntropyGenerator
   meta_transformers.BettiCurveGenerator
   meta_transformers.LandscapeGenerator


:mod:`giotto.utils`: Validation
===============================

.. automodule:: giotto.utils
   :no-members:
   :no-inherited-members:

.. currentmodule:: giotto

.. autosummary::
   :toctree: generated/
   :template: function.rst

   utils.check_diagram
   utils.validate_params
   utils.validate_metric_params

..
   :mod:`giotto.images`: Images
   ============================

..
   automodule:: giotto.images
   :no-members:
   :no-inherited-members:

..
   currentmodule:: giotto

..
   autosummary::
   :toctree: generated/
   :template: class.rst

   images.ImageInverter
   images.HeightFiltration
   images.RadialFiltration
   images.DilationFiltration
   images.ErosionFiltration
   images.SignedDistanceFiltration
   images.DensityFiltration


..
   :mod:`giotto.manifold`: Manifold learning
   =========================================

..
   automodule:: giotto.manifold
   :no-members:
   :no-inherited-members:

..
   currentmodule:: giotto

..
   autosummary::
   :toctree: generated/
   :template: class.rst

   manifold.StatefulMDS

   manifold.Kinematics