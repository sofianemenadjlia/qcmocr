#!/bin/bash


# Se déplacer dans le répertoire source d'Auto Multiple Choice
cd auto-multiple-choice_1.5.2_sources/auto-multiple-choice-1.5.2

# Construire les fichiers de version
make version_files

# Compiler le logiciel
make

# Installer Auto Multiple Choice
sudo make install

# Lancer Auto Multiple Choice
./auto-multiple-choice
