library anthrotest version '{{LIB_VERSION}}'
include anthrobase version '{{LIB_VERSION}}'
include ArmCircumferenceForAge version '{{LIB_VERSION}}' called acanthro
parameter y Decimal
parameter m Decimal
parameter l Decimal
parameter s Decimal
parameter z Decimal
parameter w Decimal

define testComputeZScore: 
    anthrobase.computeZScore(y, m, l, s)

define testComputeReverseZScore: 
    anthrobase.computeReverseZScore(z, m, l, s)

define testacanthroZscore:
    acanthro.generateZScoreArmCircumferenceForAge('female', y, w)
