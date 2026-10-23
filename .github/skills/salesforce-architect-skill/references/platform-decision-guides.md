# Platform Decision Guides & Deep Dive

> Moved out of SKILL.md (v1) to keep the skill lean. Content from the original repository
> (SalesforceDiariesBySanket/Copilot-Skills-Salesforce, MIT), updated for API 67.0 / Winter '27.
> Version-sensitive facts: `../../salesforce-developer/references/platform-release-delta.md` wins on conflict.

## Contents
- Core Philosophy · Workflow · Well-Architected deep dive · Architect Decision Guides
- Platform Fundamentals · Multi-Cloud Patterns · Agentforce · Data 360 · Deliverable Templates

## Core Philosophy

Every architectural recommendation you make should be evaluated against three pillars:

1. **Trusted** — Is the solution secure, compliant, and reliable?
2. **Easy** — Does the solution deliver value fast, and is it intentional, engaging, and maintainable?
3. **Adaptable** — Can the solution evolve with the business, and is it resilient and composable?

These are in priority order. Never sacrifice trust for ease or adaptability.

---

## Workflow: How to Approach a Salesforce Architecture Request

### Step 1: Discovery & Requirements Gathering

Before designing anything, understand the business context. Ask about (or infer from context):

- **Business processes**: What are the end-to-end workflows? (lead-to-cash, case-to-resolution, quote-to-order, etc.)
- **User personas**: Who will use the system? Internal users, partners, customers, agents?
- **Scale parameters**: Number of users, data volume expectations, transaction volumes, API call estimates
- **Existing landscape**: What Salesforce clouds/products are already licensed? What external systems exist?
- **Compliance requirements**: Industry regulations (HIPAA, GDPR, SOX, FedRAMP), data residency needs
- **Timeline and team**: Implementation timeline, team skill levels (admin-heavy vs developer-heavy)

### Step 2: Solution Design

Apply the frameworks below in order:

1. **Platform Fundamentals** — Understand multi-tenant constraints (governor limits, order of execution, metadata vs data)
2. **Well-Architected Assessment** — Evaluate against Trusted/Easy/Adaptable
3. **Decision Guide Selection** — Use the appropriate decision guide for specific design choices
4. **Integration Pattern Selection** — Choose integration patterns based on data ownership, timing, and volume
5. **Data Model Design** — Design objects, relationships, and sharing rules
6. **Security Architecture** — Layer authentication, authorization, encryption, and field-level security
7. **Automation Strategy** — Select the right tool (Flow, Apex, Platform Events) for each use case

### Step 3: Document & Diagram

Produce deliverables using Salesforce Diagrams standards (C4 model-inspired):
- **Level 1 (Marketecture)**: High-level vision showing all clouds/products
- **Level 2 (Solution Architecture)**: Integration points, data flows, technology subset
- **Level 3 (Process/Interaction)**: Sequence diagrams, time-based steps, persona interactions
- **Level 4 (Data Model / ERD)**: Entity relationships, object-level detail

### Step 4: Review & Validate

Cross-check your design against:
- Governor limits (SOQL, DML, CPU time, API limits, storage)
- Sharing and visibility model (OWD, role hierarchy, sharing rules, teams)
- Deployment strategy (change sets, CLI, DevOps Center, scratch orgs)
- Well-Architected patterns and anti-patterns

---

## Salesforce Well-Architected Framework (Deep Dive)

### TRUSTED

Solutions that protect business and stakeholders.

**Secure** (highest priority within Trusted):
- Authentication: SSO, MFA, OAuth 2.0, JWT Bearer for server-to-server
- Authorization: Principle of Least Privilege (PoLP), permission sets over profiles, permission set groups
- For Agentforce: unique agent users with PoLP, understand action security context, map private actions to end-user permissions
- Encryption: Shield Platform Encryption, TLS for data in transit
- Sharing model: OWD (most restrictive), role hierarchy, sharing rules, manual shares, teams, territory management

**Compliant**:
- Data classification and handling policies
- Audit trail, field history tracking, event monitoring
- Data residency (Hyperforce region selection)
- Retention and deletion policies

**Reliable**:
- Availability: redundancy, failover, continuity planning
- Performance: optimize throughput (bulkification, selective SOQL, indexed fields) and latency
- Scalability: data model optimization, archiving strategy (Big Objects), skinny tables, async processing
- Testing strategy: unit tests (75%+ coverage), integration tests, UAT, performance/scale testing

### EASY

Solutions that deliver value fast.

**Intentional**:
- Strategy: align architecture to business goals, not technology preferences
- Prioritization: build what matters most first
- Efficiency: avoid unnecessary complexity, use standard features before custom

**Engaging**:
- Forms: use Dynamic Forms, Screen Flows, or OmniStudio based on complexity (see Decision Guide)
- UX: Lightning App Builder, LWC for custom UI, consistent navigation and page layouts

**Maintainable**:
- Clean separation of concerns (trigger framework, service layer, selector layer)
- Naming conventions, documentation, change logs
- Technical debt tracking and remediation planning

### ADAPTABLE

Solutions that evolve with the business.

**Resilient**:
- Incident response playbooks
- Graceful error handling and retry logic
- Continuity planning for integrations and data

**Composable**:
- Application Lifecycle Management (ALM): source-driven development, CI/CD pipelines
- Environment strategy: dev → QA → UAT → staging → production (with scratch orgs for feature dev)
- Release management: versioning, rollback strategy
- Modular design: unlocked packages, loosely coupled components

---

## Architect Decision Guides

Use these guides when you face a specific design choice. The right guide depends on the question:

### 1. Record-Triggered Automation
**When**: The business needs something to happen when a record changes.
**Key decisions**:
- Same-record field update → Before-Save Flow (fastest, no DML)
- Cross-object or complex logic → After-Save Flow or Apex Trigger
- Salesforce's position: **Flow is the de-facto standard** for process automation. Workflow Rules and Process Builder are deprecated.
- Apex when: complex logic, bulkification requirements, callouts, or advanced error handling needed

**Anti-patterns to flag**:
- Multiple automation tools on the same object (e.g., Flow AND Apex trigger on same event)
- Process Builder still in use (migrate to Flow)
- Workflow Rules still in use (migrate to Flow)

### 2. Building Forms
**When**: Users need to input data.
**Options** (from simplest to most flexible):
| Tool | Best For | Skills Needed |
|------|----------|---------------|
| Dynamic Forms | Simple record pages | Admin (clicks) |
| Screen Flows | Multi-step guided processes | Admin (low-code) |
| OmniStudio | Complex industry processes | Advanced admin |
| Screen Flow + embedded LWC | Custom UI within Flow | Developer |
| Full LWC | Complete UI control | Developer |

**Key considerations**: layout flexibility, test automation capability, conditional visibility, validation, external embedding (Lightning Out), mobile support.

### 3. Data Integration
**When**: Data needs to move between Salesforce and external systems.
**First question**: Should the data be stored in Salesforce?
- Yes, event-driven → Platform Events, Change Data Capture, Pub/Sub API
- Yes, scheduled → Batch API, Bulk API 2.0, ETL tools, MuleSoft
- No, real-time access → Salesforce Connect (External Objects via OData/GraphQL)
- No, for analytics → Data 360 (formerly Data Cloud)

**Pattern categories**:
- Remote Process Invocation (Request-Reply): Salesforce calls external system synchronously
- Remote Process Invocation (Fire-and-Forget): Salesforce calls external system asynchronously
- Batch Data Synchronization: Scheduled bulk data movement
- Remote Call-In: External system calls Salesforce APIs
- Data Virtualization: Salesforce Connect / External Objects

**Key recommendation**: For cross-org and multi-org, Salesforce recommends Data 360 or MuleSoft over legacy Salesforce-to-Salesforce.

### 4. Event-Driven Architecture
**When**: You need loosely coupled, real-time communication between systems.
**Tools**: Platform Events, Change Data Capture (CDC), Pub/Sub API, AWS Event Relay
**When to use EDA**: decoupled services, messaging between orgs, real-time event responses
**Anti-patterns**: unnecessarily large payloads, using real-time platform events for batch scenarios

### 5. Migrating Changes Between Environments (ALM/DevOps)
**Spectrum from simplest to most mature**:
1. Change Sets (small teams, simple changes)
2. Salesforce CLI + Metadata API (intermediate)
3. DevOps Center (Salesforce-native CI/CD)
4. Full CI/CD with scratch orgs + unlocked packages (enterprise scale)

---

## Platform Fundamentals to Always Consider

### Governor Limits (key ones to design around)
- **SOQL queries**: 100 per synchronous transaction, 200 for async
- **DML statements**: 150 per transaction
- **CPU time**: 10,000ms synchronous, 60,000ms async
- **Heap size**: 10 MB sync, 25 MB async since Winter '27 (6/12 MB where a sandbox enforces Summer '26 limits)
- **Callouts**: 100 per transaction, 120s max timeout
- **API limits**: Per-org rolling 24-hour limit based on edition and user count
- **Data storage**: Based on edition, typically 10GB base + per-user allocation
- **Bulk API**: 15,000 batches per 24-hour rolling period

### Order of Execution
This is critical for understanding data integrity. The platform processes record saves in a specific order:
load record → field values overwritten → system validation (required fields, formats) → before-save record-triggered flows → before triggers → system validation + custom validation rules → duplicate rules → record saved to DB (not committed) → after triggers → assignment/auto-response rules → workflow rules → after-save record-triggered flows → roll-up summary → criteria-based sharing → DML committed → post-commit logic (email, async Apex).

Any fatal error during this process causes a complete rollback. Design your automation to work WITH this order, not against it.

### Metadata vs Data
- **Metadata** (configuration, deployed): Custom objects, fields, Flows, Apex classes, LWC, permission sets
- **Data** (records, loaded): Account records, Contact records, Custom Settings values
- Custom Metadata Types are metadata and can be deployed; Custom Settings are data and are org-specific

---

## Multi-Cloud Architecture Patterns

When designing across multiple Salesforce clouds:

- **Sales Cloud + Service Cloud**: Shared Account/Contact model, case escalation from opportunities, unified activity timeline
- **Sales Cloud + CPQ/Revenue Cloud**: Quote-to-cash, pricing rules, approval workflows
- **Service Cloud + Experience Cloud**: Customer self-service portals, knowledge base, case deflection
- **Marketing Cloud + Data 360**: Audience segmentation, personalization, journey orchestration
- **Agentforce across clouds**: subagent taxonomy, Multi-Agent Orchestration (GA Winter '27), Einstein Trust Layer, grounding with Data 360 / Agentforce Data Libraries

For each multi-cloud scenario, identify:
- The system of record for each entity
- Integration touch points and data flow direction
- Shared vs cloud-specific data model extensions
- Licensing implications

---

## Agentforce Architecture (see also agentforce-mcp-architecture.md)

When designing Agentforce solutions:

- **Agent User Setup**: Create unique agent users with principle of least privilege
- **Subagents (formerly topics) and Actions**: design the taxonomy deliberately; agents are now authored in Agent Script with the new Agentforce Builder (GA Summer '26). Verify current per-agent limits in the release notes before committing to a design
- **Data Grounding**: Use Data 360 for RAG (Retrieval Augmented Generation), Prompt Builder with external objects for real-time enterprise data
- **Testing**: Use Agentforce Testing Center to validate response quality and latency
- **Security**: Actions can run in elevated context — audit every action for data exposure. Map private actions to end-user permissions.
- **MCP Integration**: Model Context Protocol (Anthropic open standard) enables Agentforce to access external tools and data sources via API Catalog
- **Governance**: Enforce least-privilege via API Catalog, use MuleSoft sync for server activation/deactivation

---

## Data 360 Architecture (formerly Data Cloud)

Data 360 is a lakehouse-based data platform natively built into Salesforce:

- **Not a system of record** — it's a system of reference for decision-making and activation
- **Storage model**: Apache Iceberg + Parquet (lakehouse layer) + real-time storage layer
- **Key objects**: Data Lake Objects (DLOs) for raw ingested data, Data Model Objects (DMOs) for harmonized data
- **Ingestion patterns**: CRM Data Streams, Ingestion API, cloud storage connectors (S3/GCS/Azure Blob), streaming connectors (Kinesis/Kafka)
- **Activation**: Segments, Data Actions, calculated insights, triggered flows
- **Security**: ABAC framework with CEDAR policies, tenant isolation, encryption at rest and in transit

---

## Deliverable Templates

When producing architecture documentation, structure it as follows:

### Solution Design Document
1. Executive Summary (business context, goals, success criteria)
2. Current State Assessment (existing systems, pain points, technical debt)
3. Proposed Architecture (reference architecture diagram Level 1-2)
4. Data Model (ERD at Level 4)
5. Integration Architecture (patterns selected, sequence diagrams at Level 3)
6. Security Architecture (authentication, authorization, encryption, sharing model)
7. Automation Design (decision guide rationale for each automation)
8. DevOps Strategy (ALM approach, environments, release cadence)
9. Risks and Mitigations
10. Implementation Roadmap (phased delivery)

### Architecture Diagram Guidelines (Salesforce Diagrams Standard)
- Use clear headers describing scope and purpose
- Limit each diagram to one concept or story
- Use Salesforce Diagrams standard components and cards
- Color coding: Salesforce products (blue), external systems (gray), integration layer (green)
- Always include a legend
- Use numbered sequence flows for process/interaction diagrams

---

## Output Formats

Depending on what the user needs, produce:

- **Conversational advice**: When they ask "should I use Flow or Apex?" — give a direct recommendation with rationale from the Decision Guides
- **Architecture document (docx)**: When they need a formal deliverable — produce a well-structured markdown document
- **Presentation (pptx)**: When they need to present to stakeholders — produce a structured markdown outline suitable for slides
- **Diagrams (mermaid/SVG/HTML)**: When they need visual architecture — produce Mermaid diagrams or interactive HTML
- **Data model (ERD)**: Use Mermaid entity-relationship diagrams with Salesforce notation
- **Decision matrix**: When comparing options — produce comparison tables with the Decision Guide format

---

## Quick Reference Pointers

- **Apex coding rules (full ruleset)** → [../../Blogs/salesforce-apex-coding-rules.md](../../Blogs/salesforce-apex-coding-rules.md)
- **LWC coding rules (full ruleset)** → [../../Blogs/salesforce-lwc-coding-rules.md](../../Blogs/salesforce-lwc-coding-rules.md)
- **Developer skill (Apex, LWC, SOQL patterns)** → [../salesforce-developer/SKILL.md](../salesforce-developer/SKILL.md)
- **Data model, sharing, LDV, data skew** → [data-model-patterns.md](data-model-patterns.md)
- **Integration patterns, API selection, event-driven** → [integration-patterns.md](integration-patterns.md)
- **Well-Architected checklist, security, compliance** → [well-architected-checklist.md](well-architected-checklist.md)
