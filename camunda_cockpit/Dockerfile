FROM camunda/camunda-bpm-platform:run-latest

# Copy the custom process definition
COPY diagram_1_final.bpmn /camunda/configuration/resources/diagram_1_final.bpmn
COPY form_1.form /camunda/configuration/resources/form_1.form

# # Set the working directory
# WORKDIR /camunda

# Expose the port
EXPOSE 8080

#CMD ["camunda.sh", "-d", "/camunda/invoice-approval.bpmn", "-d", "/camunda/form_1.form"]