# Project Requirements

## Identified Problem or Need

Vehicle owners often struggle to keep track of maintenance, leading to missed services, breakdowns, and reduced lifespan of their vehicles.

## End-User Requirements

In this case the end users will be my parents as they told me currently they have the problem of forgetting to maintain their vehicles at the right intervals/mileage 
The typical end users of my maintenance tracker website are individual vehicle owners. These users need a simple and intuitive tool to help them keep track of maintenance tasks without complexity.

The system must allow users to log completed maintenance activities with details including date, mileage or engine hours, and additional notes. It should provide reminders for upcoming or overdue services based on time intervals or usage metrics. Users need the ability to update odometer or engine hour readings to keep maintenance scheduling accurate. The website should support managing multiple vehicles within one account. Lastly, users need a dashboard that summarizes recent maintenance activities and highlights upcoming service needs for a quick and easy reference.    

## Proposed Solution

A web-based tool that helps users track maintenance and receive reminders to keep their vehicles and equipment in good condition.

---

# Relevant Implications

## Improved Equipment Longevity 
When users regularly track and complete maintenance tasks like oil changes, air filter cleaning, their equipment lasts longer and performs better over time.
### Relevance to the System
This implication is relevant to my maintenance tracker project because the system is specifically designed to help users keep track of maintenance tasks, set reminders, and record service history.
### Impact / Considerations
Moving forward i will need to ensure the system supports logging, maintenance intervals, and reminders so users can consistently service their vehicles. This implication will impact the website by requiring a user friendly interface for inputting and viewing maintenance history.



## User Accountability and Reminders
This implication means that users will be more likely to complete regular maintenance tasks if they receive reminders and can see what needs to be done. By holding users accountable through alerts and tracking, the system helps prevent forgotten or delayed maintenance.
### Relevance to the System
This implication is relevant to my maintenance tracker project because one of the core features of the project is to notify users of upcoming or overdue tasks. By including reminders and a clear maintenance log, the system directly supports user accountability, helping ensure maintenance is done on time and reducing the chances of vehicle failure due to neglect.
### Impact / Considerations
Moving forward i will need to design a reliable reminder system that can send notifications based on time, usage, or user amde intervals. The system should also provide a clear and easy way for users to view, mark, and manage their maintenance tasks. This will impact the project by requiring thoughtful UX design, accurate scheduling, and possibly notification via email or push alerts to effectively keep users engaged and accountable for their maintenance.


## Data-Driven Decision Making
This implication means that by tracking and storing maintenance data over time, users can analyze their equipment’s performance and maintenance patterns. This enables them to make good decisions about when to perform maintenance, replace parts, or invest in upgrades, improving efficiency and reducing unexpected failures for the users vehicles.
### Relevance to the System
This implication is relevant to my project because my maintenance tracker collects and organizes users maintenance history and usage data. By providing access to this information, the system empowers users to identify patterns and make informed decisions about their vehicle care, which enhances the overall value and usefulness of the maintenance tracker.

### Impact / Considerations
Moving forward, the project will need to focus on good data collection, storage, and presentation. This means designing features that allow users to easily log maintenance activities and view their history in meaningful ways, such as charts or summaries. The system will also need a database solution to handle growing data over time. These considerations will impact development time and complexity but will greatly enhance user engagement and the tracker’s long-term value for the overall health of the user vehicles.


## Automated Reminders for Scheduled Maintenance

This implication refers to the need for the system to automatically notify users when maintenance tasks are due. It means the tracker must include functionality that regularly checks upcoming service dates or intervals and alerts the user without requiring manual checks from them.
### Relevance to the System
Automated reminders directly support the systems goal of ensuring good maintenance. By notifying users before tasks are due, the system helps prevent delays, reduces the chance of missed services, and keeps vehicles in optimal condition. This feature improves user trust and long term engagement within the tracker.
### Impact / Considerations
Implementing automated reminders will require reliable scheduling within the system, such as time based or usage based triggers. I will also need to consider how notifications are delivered, mail or sms and how users can customize reminder settings, and how time zones or user preferences affect scheduling. This feature increases development complexity but significantly boosts user experience and maintenance compliance.



## Data History and Maintenance Logs
this implication means the system should record and store all completed maintenance tasks over time. Each log entry would include details such as the date of service, type of maintenance performed, any parts or materials used, associated costs, and who performed the work. This creates a reliable history that users can refer back to when needed.
### Relevance to the System
Maintaining a history of all maintenance is essential for tracking the condition and service patterns of the equipment or vehicles. It allows users to monitor how well maintenance is being performed, supports troubleshooting, and provides proof of upkeep which can be important. This feature increases the overall usefulness and credibility of the maintenance tracker.
### Impact / Considerations
Implementing maintenance history requires designing a strong data storage system that can handle growing amounts of records while ensuring data integrity and security. The system must provide an easy to use interface for entering and viewing logs and possibly exporting data. Attention must be given to data backup, privacy, and user access control. This feature will increase system complexity but greatly enhances long term value and user trust over time.


---

# User Experience (UX) Principles

## Clarity and Simplicity
This principle emphasizes designing the user interface and interactions to be straightforward and easy to understand. It ensures that users can quickly see how to use the system without confusion or unnecessary complexity, reducing errors and improving overall user satisfaction.
### Relevance to the System
Clarity and simplicity are vital for a maintenance tracker because users need to quickly and easily log tasks, view schedules and understand reminders without frustration. A clear interface helps users focus on their maintenance activities rather than struggling with the system, improving efficiency.
### Impact / Considerations
To uphold clarity and simplicity, the systems design must avoid clutter, use intuitive navigation, and present information in a clean and organized manner. This may limit the amount of data or features shown at once, requiring thoughtful prioritization of content. Balancing simplicity with functionality is key, and usability testing will be important to ensure the design meets user needs without overwhelming them.

## Consistency and Familiarity
Consistency and familiarity are important for my maintenance tracker because users will benefit from predictable layouts, controls, and desgins that align with common design standards or their previous experiences. This reduces the learning, minimizes mistakes, and makes the system feel more trustworthy and easier to navigate.
### Relevance to the System
Consistency and familiarity help users quickly become comfortable with the maintenance tracker by using standard design patterns and terminology they recognize from other tools. This familiarity reduces confusion and speeds up task completion making the system more intuitive and efficient for regular use.
### Impact / Considerations
Ensuring consistency requires establishing and adhering to design guidelines for elements like buttons, colors, fonts and workflows throughout the system. Familiarity may limit innovation but improves usability, so new features should follow existing patterns where possible. Careful attention to detail and regular user testing are needed to maintain a good experience and avoid confusing users with unexpected changes.


## Feedback and Responsiveness
This principle means the system should provide timely and clear responses to user actions. Whether it’s confirming a saved entry, showing progress during loading, or alerting to errors, feedback helps users understand what is happening in the website, reduces uncertainty, and improves overall interaction for the users.
### Relevance to the System
In a maintenance tracker, timely feedback ensures users know when their actions such as logging a task or updating a schedule have been successful or if there is an issue that needs attention. Good interactions prevent confusion, build user confidence, and help maintain accurate records without getting annoyed.
### Impact / Considerations
Implementing effective feedback requires designing clear visual or haptic cues for different user actions and system states. The system must handle errors well and provide helpful messages to the user when needed. Ensuring responsiveness might require optimizing performance to avoid delays. Balancing informative feedback without overwhelming users is important to maintain a smooth and pleasant overall user experience.

