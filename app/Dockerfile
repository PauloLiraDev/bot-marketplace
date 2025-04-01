# Docker para execução no Lambda AWS
FROM public.ecr.aws/lambda/python:3.12

COPY . .
RUN pip install -r requirements.txt


# Command to run the application
CMD ["main.run"]
