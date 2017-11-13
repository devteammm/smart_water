# SmartWater
HOST: http://128.199.102.46

## Intro

  * Customer has many water device ( digital or mechanics)
  * In moment, Customer has only digital or mechanics water device
  * One water device has token, begin_value

## Actor
  * Customer
  * Water Company
  * Water Staff
  * Admin

### Staff 1
  * username: water_staff1
  * password: 1
### Staff 2
  * username: water_staff2
  * password: 1

### Customer 1
  * Use digital water device
  * username: digital_customer1
  * password: 1
  * device_token: digital_device1

### Customer 2
  * Use mechanics water device
  * username: mechanics_customer1
  * password: 1
  * device_token: mechanics_device1

### Customer 3
  * Use digital water device
  * username: digital_customer2
  * password: 1
  * device_token: digital_device2


### Customer 4
  * Use mechanics water device
  * username: mechanics_customer2
  * password: 1
  * device_token: mechanics_device2


## Digital Device API

  * username: digital_customer1
  * password: 1

  * HOST: http://128.199.102.46

  * GET: /water_device/digital/(? device_token)/(? value)

Exemple:

  ```
  get 'http://128.199.102.46/water_device/digital/digital_device1/700'
  ```
