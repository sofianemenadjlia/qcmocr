#!/bin/bash

# Function to install system prerequisites
install_system_prerequisites() {
    echo "Installing system prerequisites..."
    sudo apt update
    sudo apt install -y $(cat system_requirements.txt)
}

# Function to install Python prerequisites
install_python_prerequisites() {
    echo "Installing Python prerequisites..."
    python3 -m pip install -r py_requirements.txt
}

# Main function
main() {
    install_system_prerequisites
    install_python_prerequisites
    echo "Installation completed."
}

# Call the main function
main
