#!/bin/bash

# Updates the .env file in the event that a virus has been found.

env_file_location="/home/henry/Software/clamav_homepage/updates/.env"
echo "virusEvent=True" > $env_file_location
