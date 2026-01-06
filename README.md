# 🧰 Mattias Leadership Toolkit

Welcome to the Mattias Leadership Toolkit. This repository is a comprehensive collection of
resources designed to support leaders across various domains, including product and engineering.
It aims to help you build and maintain high-performing teams, ensure technical excellence, and
optimise delivery processes.

## 👋 Introduction

Hello, I’m [Mattias](https://www.linkedin.com/in/mattiasaltin/)!

With over 25 years of experience, I've had the privilege of working on innovative products that
touch millions of lives. My passion is empowering teams to achieve their full potential by
fostering an environment where creativity and operational excellence thrive. This toolkit
reflects my journey and the resources that have inspired me along the way.

Thank you for visiting, and I hope you find these resources as valuable as I have!

Warm regards,  
Mattias Altin  

## Getting Started

This toolkit is designed to support leaders at different stages of their journey. Here's how to get started:

### I'm a New Engineering Manager

If you're new to engineering management, start with:

1. **[Engineering Leadership Resources](engineering-leadership-resources/)** - Begin with the
   [README](engineering-leadership-resources/README.md) for an overview
2. **Essential Topics:**
   - [General Leadership](engineering-leadership-resources/org-health/general-leadership.md) - Foundational leadership skills
   - [Psychological Safety](engineering-leadership-resources/org-health/psychological-safety.md) - Creating safe environments
   - [Coaching & Mentoring](engineering-leadership-resources/org-health/coaching-and-mentoring.md) - Developing your team
3. **Recommended Reading Order:** Start with organizational health topics, then explore
   technical health and delivery execution as you gain experience

### I'm a New Product Leader

If you're new to product leadership, start with:

1. **[Product Leadership Resources](product-leadership-resources/)** - Begin with the
   [README](product-leadership-resources/README.md) for an overview
2. **Essential Topics:**
   - [Product Vision](product-leadership-resources/product-vision.md) - Understanding your North Star
   - [Product Strategy](product-leadership-resources/product-strategy.md) - Making strategic choices
   - [Coaching](product-leadership-resources/coaching.md) - Developing product talent
3. **Recommended Reading Order:** Start with leadership accountabilities (vision, strategy,
   principles), then explore management accountabilities (staffing, coaching, objectives)

### I'm Experienced, Looking for Advanced Topics

For experienced leaders seeking advanced insights:

- **Engineering:** Explore
  [Technical Excellence](engineering-leadership-resources/delivery-execution/technical-excellence-in-delivery.md),
  [Flow Efficiency](engineering-leadership-resources/delivery-execution/flow-efficiency.md),
  and
  [Metrics & Measurement](engineering-leadership-resources/delivery-execution/metrics-and-measurement.md)
- **Product:** Deep dive into
  [Product Strategy](product-leadership-resources/product-strategy.md),
  [Product Principles](product-leadership-resources/product-principles.md), and
  [Product Evangelism](product-leadership-resources/product-evangelism.md)
- **Cross-Domain:** See
  [How Engineering and Product Leadership Connect](#how-engineering-and-product-leadership-connect)
  below

### How to Use This Toolkit

This toolkit can be used in two ways:

- **Reference Guide:** Jump to specific topics as needed when facing particular challenges
- **Sequential Learning:** Read through sections systematically to build comprehensive leadership knowledge

Both approaches are valid - choose what works best for your learning style and current needs.

## Table of Contents

- [Getting Started](#getting-started)
- [Purpose](#purpose)
- [Structure](#structure)
- [Key Frameworks Referenced](#key-frameworks-referenced)
- [How Engineering and Product Leadership Connect](#how-engineering-and-product-leadership-connect)
- [License](#license)
- [Contributing](#contributing)
- [Using the Makefile](#using-the-makefile)

## Purpose

This repository serves as a resource for leaders, offering insights, best practices, and tools
to enhance leadership capabilities across various domains.

## Structure

This repository is organised into several key areas, each containing valuable resources and insights:

- **[🌱 Engineering Leadership Resources](engineering-leadership-resources/)**: A curated
  collection focused on organisational health, technical health, delivery execution, and other
  relevant topics.
- **[🌟 Product Leadership Resources](product-leadership-resources/)**: A curated collection
  focused on product vision, strategy, principles, staffing your team, coaching, setting
  objectives, and other relevant topics.

*Additional sections will be added in the future to expand the scope of this toolkit.*

## Key Frameworks Referenced

This toolkit references several frameworks that are foundational to modern leadership
practice. Here's a quick reference:

### EMPOWERED (Marty Cagan)

The EMPOWERED framework distinguishes between two types of accountabilities for product leaders:

- **Leadership Accountabilities**: Focus on product direction and strategy (vision, strategy, principles, priorities, evangelism)
- **Management Accountabilities**: Focus on people and execution (staffing, coaching, objectives)

This framework helps product leaders understand the dual nature of their role and balance
strategic thinking with operational excellence.

### GROW Model

A coaching framework with four stages:

- **Goal**: What do you want to achieve?
- **Reality**: What is the current situation?
- **Options**: What are the possible approaches?
- **Way forward**: What will you commit to doing?

The GROW model provides a structured approach to coaching conversations that helps individuals discover their own solutions.

### OKR (Objectives and Key Results)

A goal-setting framework used for alignment and focus:

- **Objectives**: Qualitative, inspirational goals that describe what you want to achieve
- **Key Results**: Quantitative, measurable outcomes that indicate progress toward the objective

OKRs help teams align around shared goals and measure progress transparently.

### DORA Metrics / Four Key Metrics

Four metrics that measure software delivery performance:

- **Deployment Frequency**: How often an organization successfully releases to production
- **Lead Time for Changes**: The amount of time it takes a commit to get into production
- **Mean Time to Recovery (MTTR)**: How long it takes an organization to recover from a failure in production
- **Change Failure Rate**: The percentage of changes that result in degraded service or require remediation

These metrics, from the book "Accelerate," help engineering leaders understand and improve their delivery capabilities.

### BICEPS Model

A model for understanding team needs and motivation:

- **Belonging**: Feeling part of a group
- **Improvement**: Making progress and growing
- **Choice**: Having autonomy and control
- **Equality**: Being treated fairly
- **Predictability**: Understanding what to expect
- **Significance**: Feeling that your work matters

The BICEPS model helps leaders understand what drives team engagement and satisfaction.

## How Engineering and Product Leadership Connect

While this toolkit is organized into separate engineering and product leadership sections, these
domains are deeply interconnected. Effective product development requires strong collaboration
between engineering and product leaders.

**Key Connections:**

- **Product Operating Model** (in Engineering section): Engineering leaders need to understand
  product operating models to align technical delivery with product strategy
- **Discovery vs Delivery**: Both domains must balance discovery (learning) with delivery (building)
- **Metrics & Measurement**: Both use metrics to understand performance, though they may focus on
  different aspects
- **Team Development**: Both engineering and product leaders share responsibilities for coaching,
  staffing, and creating healthy team environments

**Cross-References:**

- Engineering leaders working on product delivery should explore [Product Strategy](product-leadership-resources/product-strategy.md)
  and [Product Vision](product-leadership-resources/product-vision.md)
- Product leaders working with engineering teams should understand [Technical Excellence](engineering-leadership-resources/delivery-execution/technical-excellence-in-delivery.md)
  and [Flow Efficiency](engineering-leadership-resources/delivery-execution/flow-efficiency.md)
- Both domains share resources on [Coaching](engineering-leadership-resources/org-health/coaching-and-mentoring.md)
  and [Staffing/Recruiting](engineering-leadership-resources/org-health/recruiting.md)

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please see our [Contributing
Guidelines](engineering-leadership-resources/CONTRIBUTING.md) for details on how to submit
suggestions and improvements.

## Using the Makefile

The `Makefile` in this repository automates common tasks such as setting up the environment,
running scripts, and managing dependencies. Here are the available commands:

- **Set up the environment**: `make setup`
  - Sets up the virtual environment and installs dependencies.

- **Run the url_checker.py script**: `make run`
  - Runs the `url_checker.py` script using Streamlit.

- **Update dependencies**: `make freeze`
  - Updates `requirements.txt` with the current dependencies.

- **Clean up the environment**: `make clean`
  - Removes the virtual environment.

- **Display help**: `make help`
  - Displays available commands.
  