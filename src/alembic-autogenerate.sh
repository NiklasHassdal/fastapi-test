#!/bin/sh
read -p "Message: " message
alembic revision --autogenerate -m "$message"
alembic upgrade head