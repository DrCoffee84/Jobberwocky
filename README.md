# hp-devops-jobberwocky

You have been asked to implement **Jobberwocky** , a service that works as a store for job opportunities, where companies can share open positions. Candidates and sourcers should be able to query for jobs using, for example, an optional pattern for the job description. The resulting list should aggregate internal results with external sources, like LinkedIn or GitHub Jobs. Please consider **reliability** and **scalability** in your design in a general way.

## 1. Create a job posting service

Implement an application that exposes an API that lets users register new job opportunities.
- The app does not need to persist info on an external database service.
- Feel free to store jobs in memory or disk (CSV, SQLite,etc).
- Choose any API style: web‐based, REST, GraphQL, etc.
- Include a development environment to easily run tests
- Prepare the application for a basic deployment (eg: Deployment scripts, Docker, Terraform, etc.)

## 2. Create a job-searching service

Extend your application to expose another endpoint that lets users find job opportunities from the service you have already created.

## 3. Create a brief deployment strategy

Once the services are ready, create a document `RELEASE.md` and describe a strategy to deploy the service to a platform of your choice. It could be any cloud platform or a plain server.

## 4. Create additional sources

In addition to our internal job service, we want our job-searching service to consume data from additional job opportunity sources using this service: [jobberwocky-extra-source](https://github.com/avatureta/jobberwocky-extra-source-v2). Find the best way to return a response that combines the results from more than one source.


## FAQ

### Do I need to create a UI?

We will only assess the backend, but you can build one if you feel like it.

### Does the app require authentication?

No, it doesn't.

### What fields should I use for each entity?

As a developer, we expect that you design the proper structure for each entity, such as the job or the subscription entities.

### Can I use an external framework?

Yes, feel free to choose any framework that suits your needs.

### Which programming language should I use?

You may use: C++, C#, Python, Go, Java/Kotlin, Javascript/Node/Typescript, PHP, Ruby. If you’d prefer to use a different language, please let us know before getting started.

### In which language should I program?

English, please.

