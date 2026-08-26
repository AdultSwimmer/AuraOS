# Security Policy

## Overview

AuraOS is a locally oriented, continuity-focused AI architecture built around persistent memory, chronology, observation, uncertainty handling, and explicit truth-oriented behavioral constraints.

Security and privacy are important to AuraOS because the system may process conversational history, memory records, local files, and other user-provided context. The project therefore aims to favor transparency, local control, and clear boundaries around what information is stored and processed.

This document describes how to report potential security or privacy issues affecting AuraOS.

---

## Supported Versions

AuraOS is currently under active development. Security issues should be reported against the current version of the project.

| Version                     | Supported   |
| --------------------------- | ----------- |
| Current development version | Yes         |
| Older versions              | Best effort |

---

## Reporting a Vulnerability

Please **do not publicly disclose a security vulnerability before giving the project an opportunity to review it**.

If you discover a potential vulnerability involving AuraOS, please report it privately through the repository's available contact mechanism or security reporting channel.

When reporting an issue, include as much of the following information as possible:

* A clear description of the issue
* The affected component or file
* Steps required to reproduce the issue
* Expected behavior
* Actual behavior
* Potential security or privacy impact
* Whether sensitive information can be accessed, modified, exposed, or deleted
* Relevant logs or screenshots, with unrelated private information removed where possible
* Any suggested mitigation, if available

Reports made in good faith are appreciated.

---

## Areas of Particular Concern

Because AuraOS is designed around continuity and persistent context, the following areas are especially important for security review.

### Persistent Memory

Potential issues involving:

* unauthorized access to stored memory
* unintended retention of user information
* memory records being exposed to other users or processes
* corruption or manipulation of stored chronology
* failure to properly separate identities or sessions

should be reported.

### Local Data and Files

AuraOS may interact with locally stored:

* conversation records
* JSON memory files
* application configuration
* logs
* user-provided documents or other artifacts

Any vulnerability that could expose, overwrite, delete, or improperly access local data is considered important.

### Identity and Session Handling

The system architecture includes mechanisms related to user identification and persistent state.

Potential problems involving:

* identity collisions
* unauthorized access to another user's stored context
* session confusion
* incorrect memory association
* hashing or identifier weaknesses

should be reported.

### Model and Processing Boundaries

AuraOS may use language models and local processing pipelines as components of a broader architecture.

Relevant security concerns include:

* prompt injection affecting system behavior or stored memory
* malicious content influencing persistent records
* unsafe processing of imported conversation files
* model-generated instructions causing unintended actions
* data escaping intended local processing boundaries

---

## Privacy Principles

AuraOS is intended to support greater continuity without treating user context as disposable.

That makes privacy especially important.

The project should strive to:

* minimize unnecessary exposure of user data
* keep local information under user control where practical
* make persistent storage understandable and inspectable
* distinguish user-provided material from generated interpretation
* avoid silently promoting generated content into authoritative records
* preserve uncertainty where information is incomplete
* make corrections and contradictions visible rather than silently rewriting history

These principles do not guarantee that the software is free from vulnerabilities. They describe the intended direction of the architecture.

---

## Responsible Disclosure

If a vulnerability is reported:

1. The issue should be reviewed to determine whether it is reproducible.
2. The affected component and potential impact should be assessed.
3. A fix or mitigation should be developed where practical.
4. Public disclosure should occur only after the issue has been addressed or sufficient time has been provided for remediation.

Security findings may be documented publicly after remediation when doing so helps users understand the issue without unnecessarily exposing them to active exploitation.

---

## Scope

This policy applies to security and privacy issues directly affecting the AuraOS codebase and its documented local architecture.

It does not apply to:

* unrelated third-party software
* vulnerabilities in external model providers
* vulnerabilities in external services not controlled by AuraOS
* general disagreements with model output or interpretations that do not involve a security or privacy vulnerability

However, issues involving the interaction between AuraOS and external components may still be useful to report if they create a demonstrable security or privacy risk within AuraOS itself.

---

## Good-Faith Research

Good-faith security research is welcome.

Researchers are encouraged to:

* avoid accessing data that does not belong to them
* avoid destructive testing against systems containing real user data
* provide reproducible information where possible
* allow reasonable time for review before public disclosure

The goal is to identify weaknesses and improve the architecture without unnecessarily exposing users or data to harm.

---

## Security Philosophy

AuraOS is built around the idea that continuity, memory, chronology, and truth-oriented reasoning should be treated as explicit architectural concerns.

Security supports that same objective.

A continuity system is only useful if users can understand where their information exists, how it is associated with them, and whether the system can be trusted not to expose or corrupt it.

For AuraOS, security is therefore not separate from system integrity. Protecting the confidentiality, integrity, provenance, and continuity of user information is part of protecting the architecture itself.
