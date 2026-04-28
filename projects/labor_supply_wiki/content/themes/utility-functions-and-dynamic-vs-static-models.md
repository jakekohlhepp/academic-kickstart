---
title: Utility functions and dynamic vs. static models
slug: utility-functions-and-dynamic-vs-static-models
deck: A model-side guide to the utility functions, state variables, and static versus dynamic choices that sit underneath labor-supply estimates in the literature.
featured_articles: blinder-weiss-1976-human-capital-and-labor-supply|macurdy-1981-life-cycle-labor-supply|browning-deaton-irish-1985-life-cycle-labor-supply-demands|imai-keane-2004-intertemporal-labor-supply-human-capital|wallenius-2011-human-capital-bias-ies-labor|hausman-ruud-1984-family-labor-supply-with-taxes|dickens-lundberg-1993-hours-restrictions-and-labor-supply|chetty-2012-bounds-on-elasticities|keane-rogerson-2015-reconciling-micro-macro-elasticities|kleven-kreiner-larsen-sogaard-2025-dynamic-returns-to-effort|chen-ding-list-mogstad-2025-job-flexibility
---
## Why this page exists

A lot of disagreement in the labor-supply literature is really disagreement about the model underneath the estimate. Two papers can both be credible and still speak past each other because one assumes a static hours choice and the other assumes a dynamic problem with state variables, adjustment costs, or fixed job packages.

## Static models: the classic starting point

In a static model, the worker chooses labor supply for the current period by trading off consumption against leisure or hours disutility. Utility is often written as something like `u(c, h)` or `u(c, l)` where `l` is leisure. The basic appeal is clarity: if wages change today, how do hours or participation change today?

This framework sits behind a lot of canonical tax-and-labor-supply work, including [Family Labor Supply with Taxes](../articles/hausman-ruud-1984-family-labor-supply-with-taxes.html). These models are often powerful for policy simulation, but they lean heavily on assumptions about utility shape, household aggregation, and whether workers can freely choose hours.

## Dynamic models: labor supply with state variables

Dynamic models treat current work decisions as affecting the future. Once experience, human capital, promotions, search, health, or caregiving status matter tomorrow, the worker is solving more than a one-period optimization problem.

- [Human Capital and Labor Supply: A Synthesis](../articles/blinder-weiss-1976-human-capital-and-labor-supply.html) is an early statement that labor supply and human-capital accumulation must be modeled jointly.
- [An Empirical Model of Labor Supply in a Life-Cycle Setting](../articles/macurdy-1981-life-cycle-labor-supply.html) is the classic panel-data life-cycle estimate of intertemporal substitution.
- [Micro versus Macro Labor Supply Elasticities: The Role of Dynamic Returns to Effort](../articles/kleven-kreiner-larsen-sogaard-2025-dynamic-returns-to-effort.html) is a modern example where effort today changes future wages and advancement.
- [Reservation Wages and Workers' Valuation of Job Flexibility](../articles/chen-ding-list-mogstad-2025-job-flexibility.html) shows how dynamic modeling matters when reservation wages vary over time and workers repeatedly choose whether to work.

## Common utility-function choices in the literature

The same broad labor-supply question can be estimated with very different utility objects.

- Separable consumption-leisure utility: common in static models because it keeps interpretation simple.
- Intertemporally separable but dynamically linked utility: common in life-cycle models where the state evolves through assets, experience, or wages.
- Household utility functions: used when spouses' choices are modeled jointly and taxes or care obligations interact inside the household.
- Fixed-cost or participation-cost utility: used when entering work carries a discrete cost, which is often crucial for extensive-margin responses.
- Discrete-choice job-package utility: used when workers choose among jobs or shifts with fixed hours, amenities, and scheduling rules rather than a smooth hours margin. [Labor Supply with Hours Restrictions](../articles/dickens-lundberg-1993-hours-restrictions-and-labor-supply.html) is a clear benchmark here.

## Static versus dynamic is not just a technical detail

The model choice changes the elasticity object itself.

- Static models are usually closest to short-run within-period substitution.
- Dynamic models are usually needed when the researcher cares about reentry, retention, career effects, human-capital accumulation, or persistent caregiving and health shocks.
- Discrete-choice models are often needed when the feasible set is lumpy because jobs come in packages.

That is why [Bounds on Elasticities With Optimization Frictions](../articles/chetty-2012-bounds-on-elasticities.html) remains so important. Even if utility is well behaved, observed choices may still reflect friction, inattention, or coarse choice sets rather than the frictionless optimum.

## A practical reading rule

When reading a labor-supply estimate, ask four questions first.

1. What is inside utility: only consumption and leisure, or also fixed costs, amenities, or household interactions?
2. Is the model static or dynamic?
3. What are the state variables: assets, wages, experience, children, health, or job matches?
4. Is the worker choosing smooth hours, participation, or among discrete job packages?

Those questions usually tell you more than the headline elasticity.

## How this page fits with the rest of the wiki

This page is the model companion to [estimation strategies and relative credibility](../themes/estimation-strategies-and-relative-credibility.html). That page is about research design credibility. This page is about the behavioral structure underneath the estimate.

For deeper dynamic routes, use [human capital and labor supply](../themes/human-capital-and-labor-supply.html), [life-cycle structural estimation](../themes/life-cycle-structural-estimation.html), and [indivisible labor and extensive-margin models](../themes/indivisible-labor-and-extensive-margin.html).
