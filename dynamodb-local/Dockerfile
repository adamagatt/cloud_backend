FROM amazon/dynamodb-local

# Upload db dump file and provide access to container user
COPY ./anything_ap-southeast-2.db /home/dynamodblocal/.
USER root
RUN chown dynamodblocal ./anything_ap-southeast-2.db
USER dynamodblocal

CMD ["-jar", "DynamoDBLocal.jar"]