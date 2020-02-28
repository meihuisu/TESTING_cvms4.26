#!/bin/sh


run() {

paste -d ',' BILLY_DATA/${STUB}_Billy_25_vs.csv RESULT/${STUB}_ucvm_25_vs.csv > ${STUB}_compare_vs.csv

paste -d ',' BILLY_DATA/${STUB}_Billy_25_vp.csv RESULT/${STUB}_model_25_vp.csv > ${STUB}_compare_vp.csv

}

####### MAIN #######

STUB='Santa_Maria_Basin'
run
STUB='China_Lake_Basin'
run
STUB='Continental_Borderland'
run
STUB='E_Mojave'
run
STUB='Eastern_California_Shear_Zone'
run
STUB='Great_Valley'
run
STUB='Los_Angeles_Basin'
run
STUB='Ophiolitic_Terranes'
run
STUB='Peninsular_Range_Batholith'
run
STUB='Proterozoic_Terranes'
run
STUB='Salton_Trough'
run
STUB='Sierra_Nevada_Batholith'
run
STUB='Tehachapi_Mountains'
run
STUB='Ventura_Basin'
run
STUB='W_Mojave'
run

