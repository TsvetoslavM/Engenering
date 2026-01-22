# Design Patterns (Overview)

## 1) Singleton
Ensures a class has only one instance and provides a global access point to it. Commonly used for shared resources like configuration, logging, or a connection manager.

## 2) Factory Method
Defines an interface for creating objects, but lets subclasses decide which class to instantiate. Helps when object creation logic varies by environment or input and you want to avoid large conditional blocks.

## 3) Strategy
Defines a family of algorithms, encapsulates each one, and makes them interchangeable at runtime. Useful when you want to switch behavior (e.g., pricing rules, routing logic, filtering) without changing callers.

## 4) Observer
Defines a one-to-many dependency so when one object changes state, all dependents are notified. Often used for event systems, pub/sub messaging, and UI updates.

## 5) Decorator
Attaches additional responsibilities to an object dynamically. Useful for adding behavior like caching, logging, authorization, or rate limiting without modifying the original object.
