library anthrobase version '{{LIB_VERSION}}'
using FHIR version '{{FHIR_VERSION}}'
include FHIRHelpers version '{{FHIR_VERSION}}' called FHIRHelpers



// https://github.com/WorldHealthOrganization/anthro/blob/9f75f7ab10f371558fb103f701740a7b4fb37143/R/z-score-helper.R#L12

define function computeZScore(y Decimal, m Decimal, l Decimal, s Decimal):
    (((y / m)^l - 1) div (s * l)) as Decimal

define function computeReverseZScore(z Decimal,m Decimal,l Decimal,s Decimal):
    (m * (z*s*l-1)^(1/l)) as Decimal
