# NYCT NoWriter MVP - Two-Stage Process Enhancement
## Product Requirements Document (PRD)

---

## Executive Summary

The NYCT NoWriter MVP is being enhanced from a single-stage to a two-stage process to improve the quality and efficiency of grant proposal rejection workflows. This enhancement addresses feedback from program directors who need better proposal understanding before generating rejection communications, while maintaining the application's stateless security architecture.

**Current State**: Single-stage process that generates both internal rationales and external communications simultaneously after uploading proposal, selecting reason codes, and adding staff notes.

**Future State**: Two-stage process where Stage 1 provides AI-generated proposal summaries for director review, and Stage 2 generates refined internal rationales and external communications based on director input and rejection reasoning.

---

## Problem Statement

### Current Challenges
1. **Limited Proposal Understanding**: Program directors must fully read and understand proposals before making rejection decisions, which is time-consuming for the 600-800 annual rejections
2. **Generic Rationales**: Current single-stage process produces rationales that may not accurately reflect the specific issues with each proposal
3. **Workflow Mismatch**: Directors need to understand proposals before determining rejection reasons, but current flow requires reason selection upfront
4. **Format Inconsistency**: Internal rationales don't consistently follow NYCT's preferred format of proposal summary + specific rejection reasons

### Business Impact
- **Time Inefficiency**: Directors spend excessive time reading full proposals before determining rejection approach
- **Quality Inconsistency**: Rationales may not accurately reflect proposal content or director's specific concerns
- **Process Friction**: Current workflow doesn't match natural decision-making process

---

## Solution Overview

### Two-Stage Process Design

**Stage 1: Proposal Analysis**
- Upload proposal document
- AI generates concise proposal summary
- Director reviews summary to understand key elements
- No data persistence between stages (maintains stateless architecture)

**Stage 2: Rejection Generation**
- Director inputs specific rejection reasons based on Stage 1 understanding
- AI generates internal rationale (concise, factual, NYCT format)
- AI generates external communication (following standardized templates)
- Both outputs available for copy/download

---

## User Stories

### Primary User: NYCT Program Director

**Stage 1 Stories:**
- As a program director, I want to upload a proposal and receive an AI-generated summary so that I can quickly understand the key elements without reading the entire document
- As a program director, I want the summary to highlight key proposal details (organization, amount requested, program description, target population) so that I can make informed rejection decisions
- As a program director, I want to proceed to Stage 2 with the proposal context so that I can generate targeted rejection communications

**Stage 2 Stories:**
- As a program director, I want to input specific rejection reasons based on my Stage 1 review so that the AI can generate accurate, contextual rationales
- As a program director, I want to generate an internal rationale that follows NYCT's format (proposal summary + specific rejection reasons) so that it's consistent with our documentation standards
- As a program director, I want to generate an external communication that follows our standardized templates so that applicants receive professional, appropriate responses
- As a program director, I want both outputs to be available for immediate copy/download so that I can use them in my existing workflows

### Secondary User: NYCT Management

**Governance Stories:**
- As NYCT management, I want to ensure the application remains stateless so that no sensitive proposal data is stored or persisted
- As NYCT management, I want to track usage metrics across both stages so that we can measure efficiency gains and process adoption
- As NYCT management, I want the application to integrate smoothly with existing workflows so that adoption is seamless

---

## Functional Requirements

### Stage 1: Proposal Analysis

#### FR-1.1: Document Upload
- **Requirement**: Support PDF and Word document upload (max 10MB)
- **Behavior**: Same drag-and-drop interface as current implementation
- **Validation**: File type and size validation with user-friendly error messages
- **Processing**: Extract full text content for AI analysis

#### FR-1.2: AI Proposal Summary Generation
- **Requirement**: Generate concise, structured proposal summary
- **Content Elements**:
  - Organization name and mission
  - Grant amount requested
  - Program/project description (2-3 sentences)
  - Target population and geographic scope
  - Key outcomes and metrics proposed
  - Timeline and implementation approach
- **Format**: Structured summary (150-200 words maximum)
- **Performance**: Generate summary within 10 seconds (P95)

#### FR-1.3: Summary Review Interface
- **Requirement**: Display AI-generated summary in clean, readable format
- **Features**:
  - Clear section headers for each summary element
  - Easy-to-scan formatting
  - Option to regenerate summary if needed
  - "Proceed to Stage 2" action button
- **Accessibility**: Screen reader compatible, keyboard navigation support

#### FR-1.4: Stage Transition
- **Requirement**: Seamless transition from Stage 1 to Stage 2
- **Behavior**: Carry forward proposal context without data persistence
- **Implementation**: Pass summary and proposal data through session state
- **Security**: No server-side storage of proposal content

### Stage 2: Rejection Generation

#### FR-2.1: Rejection Reason Input
- **Requirement**: Enhanced reason code selection and free-form input
- **Components**:
  - Dropdown with 8 existing NYCT board-reportable decline codes
  - Free-form text area for specific rejection details (500 character limit)
  - Context from Stage 1 summary visible for reference
- **Validation**: Both reason code and specific details required

#### FR-2.2: Internal Rationale Generation
- **Requirement**: Generate internal rationale following NYCT format
- **Structure**:
  - Proposal Summary section (from Stage 1, lightly edited for context)
  - Rejection Reasoning section (specific, factual reasons)
  - Board-reportable reason code clearly identified
  - Professional, concise tone (150-200 words total)
- **Quality Requirements**:
  - Factual and specific to proposal content
  - Avoids generic language
  - Consistent with NYCT voice and standards

#### FR-2.3: External Communication Generation
- **Requirement**: Generate external applicant communication
- **Format**: Follow existing NYCT standardized templates
- **Content**:
  - Professional, respectful tone
  - Generic reasoning (no specific proposal details)
  - Encouragement for future applications where appropriate
  - Standard NYCT contact information and resources
  - Length: 90-120 words
- **Customization**: Ability to select from multiple template variations

#### FR-2.4: Output Management
- **Requirement**: Present both outputs for review and use
- **Features**:
  - Side-by-side display of internal rationale and external communication
  - Individual copy-to-clipboard functionality
  - Combined download as formatted document
  - Edit capability for minor adjustments
  - Generation time display for performance tracking

### Cross-Stage Requirements

#### FR-3.1: Progress Tracking
- **Requirement**: Clear indication of current stage and progress
- **Implementation**: Enhanced progress indicator showing Stage 1 and Stage 2 steps
- **Features**: Stage completion status, ability to return to previous stage if needed

#### FR-3.2: Session Management
- **Requirement**: Maintain session state without data persistence
- **Behavior**: Store proposal context in browser session storage
- **Security**: Automatic session clearing on browser close/refresh
- **Timeout**: 30-minute session timeout for security

#### FR-3.3: Reset Functionality
- **Requirement**: Clear all data and return to Stage 1 beginning
- **Trigger**: Explicit "Start New Process" button
- **Behavior**: Clear all session data, reset UI state
- **Confirmation**: User confirmation dialog before clearing

---

## Non-Functional Requirements

### Performance Requirements
- **NFR-1**: Stage 1 summary generation completed in <10 seconds (P95)
- **NFR-2**: Stage 2 rationale generation completed in <8 seconds (P95)
- **NFR-3**: Application remains responsive during AI processing
- **NFR-4**: File upload processing completed in <5 seconds for 10MB files

### Security Requirements
- **NFR-5**: No persistent storage of proposal content or generated outputs
- **NFR-6**: Session data cleared automatically on browser close
- **NFR-7**: HTTPS encryption for all data transmission
- **NFR-8**: Password protection capability for future implementation

### Reliability Requirements
- **NFR-9**: 99.5% uptime during business hours (9 AM - 6 PM EST)
- **NFR-10**: Graceful error handling with user-friendly messages
- **NFR-11**: Automatic retry capability for failed AI generations
- **NFR-12**: Data validation at each stage to prevent errors

### Usability Requirements
- **NFR-13**: Intuitive two-stage workflow with clear navigation
- **NFR-14**: Mobile-responsive design for tablet use
- **NFR-15**: Accessibility compliance (WCAG 2.1 AA)
- **NFR-16**: Consistent with MTM branding and design system

### Scalability Requirements
- **NFR-17**: Support for 600-800 rejections annually (2-3 daily peak)
- **NFR-18**: Concurrent user support (up to 5 simultaneous users)
- **NFR-19**: Stateless architecture to support horizontal scaling

---

## User Flow

### Stage 1: Proposal Analysis Flow
1. **Landing**: User arrives at application homepage
2. **Upload**: User uploads proposal document via drag-and-drop or file browser
3. **Processing**: System extracts text and validates file
4. **Generation**: AI analyzes proposal and generates structured summary
5. **Review**: User reviews AI-generated proposal summary
6. **Decision**: User decides to proceed to Stage 2 or regenerate summary
7. **Transition**: User clicks "Proceed to Stage 2" to continue

### Stage 2: Rejection Generation Flow
1. **Context**: Stage 1 summary displayed for reference
2. **Input**: User selects reason code from dropdown
3. **Details**: User provides specific rejection reasoning (free text)
4. **Generation**: AI generates internal rationale and external communication
5. **Review**: User reviews both generated outputs
6. **Action**: User copies/downloads outputs or makes minor edits
7. **Complete**: User completes process or starts new proposal

### Alternative Flows
- **Regeneration**: User can regenerate outputs at any stage with different inputs
- **Navigation**: User can return to Stage 1 from Stage 2 if needed
- **Reset**: User can clear all data and start over at any point
- **Error Recovery**: Clear error messages with suggested actions for resolution

---

## Success Metrics

### Primary Success Metrics
- **Time Efficiency**: Reduce average time per rejection from current baseline to <15 minutes
- **Process Adoption**: 90%+ of program directors use two-stage process within 3 months
- **Quality Improvement**: 80%+ of generated rationales require minimal manual editing
- **Volume Handling**: Successfully process 600-800 rejections annually

### Secondary Success Metrics
- **Stage 1 Effectiveness**: 85%+ of summaries provide sufficient information for rejection decisions
- **User Satisfaction**: 4.5/5 average user satisfaction rating
- **Technical Performance**: <10 second average generation time for both stages
- **Error Rate**: <5% failed generations requiring manual retry

### Analytics and Tracking
- **Usage Patterns**: Track completion rates for each stage
- **Performance Metrics**: Monitor generation times and error rates
- **User Behavior**: Analyze regeneration frequency and edit patterns
- **Content Quality**: Track manual edit rates as quality indicator

---

## Implementation Phases

### Phase 1: Core Two-Stage Architecture (Weeks 1-3)
**Scope**: Implement basic two-stage workflow
- Modify existing upload component for Stage 1
- Create proposal summary generation and display
- Implement stage transition logic
- Update progress indicators for two-stage flow
- Basic session management (no persistence)

**Deliverables**:
- Working Stage 1 with mock AI summary generation
- Stage transition functionality
- Updated UI with stage indicators
- Session state management

**Acceptance Criteria**:
- User can upload document and receive summary
- User can proceed to Stage 2 with context
- No data persisted between sessions
- Clear stage progression indication

### Phase 2: Enhanced Generation Logic (Weeks 4-5)
**Scope**: Implement improved AI generation for both stages
- Enhanced proposal summary generation (Stage 1)
- Refined internal rationale generation following NYCT format
- External communication generation with template options
- Improved prompt engineering for quality

**Deliverables**:
- Production-ready AI integration
- NYCT-formatted internal rationales
- Template-based external communications
- Quality validation logic

**Acceptance Criteria**:
- Summaries include all required elements
- Internal rationales follow NYCT structure
- External communications match templates
- Generation times meet performance requirements

### Phase 3: User Experience Enhancement (Weeks 6-7)
**Scope**: Polish user interface and experience
- Enhanced UI for two-stage workflow
- Improved output display and management
- Advanced edit capabilities
- Better error handling and user feedback

**Deliverables**:
- Polished two-stage interface
- Enhanced output management tools
- Comprehensive error handling
- Improved accessibility features

**Acceptance Criteria**:
- Intuitive navigation between stages
- Easy output management and editing
- Clear error messages and recovery
- Full accessibility compliance

### Phase 4: Production Readiness (Weeks 8-9)
**Scope**: Prepare for production deployment
- Performance optimization
- Comprehensive testing
- Security hardening
- Documentation and training materials

**Deliverables**:
- Performance-optimized application
- Comprehensive test suite
- Security audit results
- User training documentation

**Acceptance Criteria**:
- All performance requirements met
- Security requirements validated
- User acceptance testing completed
- Training materials delivered

---

## Acceptance Criteria

### Stage 1 Acceptance Criteria
- **AC-1.1**: User can upload PDF/Word documents up to 10MB successfully
- **AC-1.2**: System generates proposal summary within 10 seconds containing all required elements
- **AC-1.3**: Summary includes organization name, grant amount, program description, target population, outcomes, and timeline
- **AC-1.4**: User can regenerate summary if unsatisfied with initial result
- **AC-1.5**: User can proceed to Stage 2 with proposal context maintained
- **AC-1.6**: No proposal data is persisted in server storage

### Stage 2 Acceptance Criteria
- **AC-2.1**: User can select from 8 existing NYCT reason codes
- **AC-2.2**: User can input specific rejection details (up to 500 characters)
- **AC-2.3**: System generates internal rationale following NYCT format (summary + reasons)
- **AC-2.4**: System generates external communication following standardized templates
- **AC-2.5**: Both outputs generated within 8 seconds
- **AC-2.6**: User can copy individual outputs to clipboard
- **AC-2.7**: User can download combined outputs as formatted document
- **AC-2.8**: User can make minor edits to generated content

### Cross-Stage Acceptance Criteria
- **AC-3.1**: Progress indicator clearly shows current stage and completion status
- **AC-3.2**: User can navigate back to previous stage if needed
- **AC-3.3**: Session data automatically clears on browser close/refresh
- **AC-3.4**: "Start New Process" function clears all data and returns to Stage 1
- **AC-3.5**: Application remains responsive during AI processing
- **AC-3.6**: Error handling provides clear, actionable guidance
- **AC-3.7**: Mobile/tablet interface remains fully functional

### Quality Acceptance Criteria
- **AC-4.1**: Generated summaries accurately reflect proposal content
- **AC-4.2**: Internal rationales are factual, specific, and professional
- **AC-4.3**: External communications maintain appropriate tone and messaging
- **AC-4.4**: No sensitive proposal details appear in external communications
- **AC-4.5**: Generated content requires minimal manual editing (target <20%)
- **AC-4.6**: Consistency maintained across multiple generations for same proposal

### Performance Acceptance Criteria
- **AC-5.1**: Stage 1 summary generation: <10 seconds (P95)
- **AC-5.2**: Stage 2 rationale generation: <8 seconds (P95)
- **AC-5.3**: File upload processing: <5 seconds for 10MB files
- **AC-5.4**: Application load time: <3 seconds on standard internet connection
- **AC-5.5**: Concurrent user support: Up to 5 simultaneous users without degradation
- **AC-5.6**: Error rate: <5% failed generations

---

## Technical Considerations

### Architecture Changes
- **Session Management**: Implement robust browser session storage for proposal context
- **State Management**: Enhanced React state management for two-stage workflow
- **API Design**: Separate endpoints for Stage 1 summary and Stage 2 generation
- **Error Handling**: Comprehensive error handling with user recovery options

### AI/LLM Integration
- **Prompt Engineering**: Separate optimized prompts for Stage 1 summaries and Stage 2 generation
- **Context Management**: Efficient passing of proposal context between stages
- **Quality Controls**: Validation logic to ensure output quality and consistency
- **Fallback Mechanisms**: Retry logic and graceful degradation for AI failures

### Security & Privacy
- **Stateless Design**: Maintain no persistent storage of proposal content
- **Session Security**: Secure session management with automatic cleanup
- **Data Transmission**: Encrypted transmission of all proposal data
- **Access Controls**: Foundation for future password protection implementation

### Integration Points
- **Existing Workflow**: Seamless integration with current NYCT proposal review processes
- **Output Formats**: Compatible with existing documentation and communication tools
- **Analytics**: Enhanced metrics collection for two-stage process monitoring
- **Future Enhancements**: Architecture supports planned password protection and advanced features

---

## Risk Assessment

### High Risk Items
- **User Adoption**: Risk that directors prefer single-stage simplicity
  - *Mitigation*: User testing and feedback integration, optional single-stage fallback
- **AI Quality**: Risk that two-stage process produces lower quality outputs
  - *Mitigation*: Enhanced prompt engineering, A/B testing, quality validation
- **Performance Impact**: Risk that two-stage process is significantly slower
  - *Mitigation*: Optimization focus, performance monitoring, user expectations

### Medium Risk Items
- **Session Management**: Risk of losing proposal context between stages
  - *Mitigation*: Robust session handling, user-friendly error recovery
- **UI Complexity**: Risk that two-stage interface is confusing
  - *Mitigation*: Intuitive design, clear progress indicators, user testing

### Low Risk Items
- **Technical Implementation**: Well-understood technical changes
- **Security Model**: Maintains existing stateless security approach
- **Integration**: Minimal impact on existing workflows and systems

---

## Appendices

### Appendix A: Current vs. Future State Comparison

| Aspect | Current State | Future State |
|--------|--------------|-------------|
| Process Stages | Single stage | Two stages |
| Proposal Review | Manual full reading | AI-generated summary |
| Decision Making | Upfront reason selection | Informed reason selection |
| Internal Rationale | Generic structure | NYCT-specific format |
| External Communication | AI-generated | Template-based generation |
| Time Investment | High initial reading time | Distributed across stages |
| Quality Control | Limited context awareness | Context-informed generation |

### Appendix B: NYCT Internal Decline Memo Format Specification

**Required Components**:

1. **Proposal Summary Section** (First Paragraph):
   - Organization name and mission
   - Grant amount requested  
   - Specific program or project being funded
   - Target population and geographic scope
   - Key deliverables or outcomes proposed

2. **Decline Rationale Section** (Second Paragraph):
   - 3-4 specific, factual components that support the decline decision
   - Must be substantive enough to understand without referring to original proposal
   - Include concrete details from the proposal (not generic statements)
   - Reference specific gaps, misalignments, or concerns
   - Should directly relate to the selected board-reportable reason code

**Format Requirements**:
- **Length**: 150-200 words maximum
- **Reading Time**: Must be digestible within 5 minutes
- **Tone**: Factual, professional, concise
- **Language**: Avoid "fluffy" or overly diplomatic phrasing
- **Focus**: Program-specific issues rather than organizational concerns

**Quality Standards**:
- Must contain enough context that a reader can understand the decision without the original proposal
- Should clearly articulate why this specific request doesn't align with NYCT priorities
- Avoid boilerplate language that could apply to any proposal
- No unnecessary references to board processes or general funding constraints

**Real Examples from NYCT**:

**Example 1 - Capacity Concerns**:
"Astoria Cats Rescue, founded in 2014, feeds and cares for 18 cat colonies across Astoria, completes spay/neutering, and facilitates adoptions through events and fostering. This $150,000 request is to support the lease of a professional facility and purchase supplies, materials, and a new vehicle. The one-year $285,000 project budget includes $82,000 for the lease and utilities, $24,000 for facility start-up costs, and $16,000 for a new vehicle. ACR's current operating budget is $123,000.

I recommend this request be declined for capacity reasons. ACR's aspirational FY25 budget is more than double its current operating budget and it relies almost exclusively on community donations; I'm not convinced it can fundraise the balance. Moreover, the proposal does not provide strong evidence that ACR will be able to adjust to a bigger space, which comes with higher demand; it employs five part-time staff and uses volunteers for most of its programming."

**Example 2 - Strategic Misalignment**:
"Community Food Advocates seeks a $125,000 grant from the Trust to support its Youth Food Advocates Leadership Development Internship program, serving a small cohort of 15 NYC public high school students each year. The goal of the program is to create a career pipeline for future advocates of color.

While the program sounds like a meaningful experience, the program does not fit into the systemic priorities of our Human Services grant strategy. The main expected outcome of the program is student retention from year to year; there are no expected outcomes or outputs around specific policy or program activities regarding hunger alleviation or food systems improvements. Additionally, though the program is intended to create a pipeline of diverse young food justice leaders, there are no specific activities or goals around career pathways with reference to future job placements or employer partner engagement."

**Example 3 - Operational Support/Unclear Objectives**:
"MediSys Health Network, comprised of Jamaica and Flushing Hospital Medical Center, is an integrated healthcare system with 10 primary care clinics and one nursing home that provides an array of services across 37 zip codes in Queens and Brooklyn. MediSys Health Network requests a two-year $300,000 grant to implement a pilot program in the new Center for Wellness and Health in Jamaica, Queens. The Center for Wellness and Health includes a fitness center, teaching kitchen, greengrocer pantry and patient-centered care from an interdisciplinary team to Medicaid beneficiaries.

While Medisys's new center aims to address access to comprehensive and coordinated care, their proposal does not merit support. Medisys requested funding for operational costs within the health center, which The Trust does not fund. Additionally, they did not supply goals and objectives which they would achieve within the grant period. And finally, the proposal is devoid from connecting the work of the proposed center with the work of the Hospital."

**Example 4 - Outside Guidelines/Sustainability Concerns**:
"New Neighbors Partnership is dedicated to helping refugee and asylum-seeking families create sustainable networks of community support as they resettle in the New York area. New Neighbors' core initiative is a giving program, through which newcomer families are matched with local families who can share ongoing clothing hand-me-downs. The organization requests $20,000 to support their ongoing activities, specifically the clothing partnership program, by allowing them to increase the hours of their part-time program coordinator and part-time resource coordinator.

New Neighbors' overarching goal of providing in-kind clothing and social support is important for newly arrived families, but it is not systemic or in line with our human services grant strategy, which focuses on supporting research, policy, and programs to move individuals to stability/independence and advocating for wide-ranging or quality services for low-income individuals and families. Additionally, this specific proposal seems to focus on bolstering the organization's capacity by increasing the number of working hours for two of their employees. There are no plans for sustaining this increase after the grant period."

**Key Patterns from Real NYCT Examples**:
1. **Opening**: Always starts with organization background and specific request details
2. **Specificity**: Includes exact dollar amounts, budget breakdowns, and program specifics  
3. **Direct Language**: Uses "I recommend this request be declined" rather than passive voice
4. **Concrete Reasons**: Cites specific deficiencies (e.g., "more than double its current operating budget", "no expected outcomes or outputs", "did not supply goals and objectives")
5. **Strategy Alignment**: Explicitly states how proposal doesn't align with NYCT's grant strategies
6. **No Fluff**: Avoids diplomatic language about "difficult decisions" or "limited resources"
7. **Length**: Ranges from 100-200 words, with most around 150-180 words

### Appendix C: External Communication Templates

**Standard Template Elements**:
- Greeting and appreciation
- General decline notification
- Generic reasoning category
- Future opportunity encouragement
- Contact information
- Professional closing

**Template Variations**:
- Standard decline
- Strategic priority mismatch
- Geographic scope limitation
- Capacity/readiness concerns

### Appendix D: Success Metrics Detail

**Baseline Measurements** (to be established):
- Current time per rejection
- Current quality ratings
- Current user satisfaction
- Current error/revision rates

**Target Improvements**:
- 50% reduction in time per rejection
- 25% improvement in quality ratings
- 90% user satisfaction score
- 75% reduction in revision requirements

---

*Document Version: 1.1*
*Last Updated: August 12, 2025*
*Document Owner: Product Requirements Team*
*Stakeholder Approval: Pending*

**Version History:**
- v1.0 (August 12, 2025): Initial PRD based on meeting transcript analysis
- v1.1 (August 12, 2025): Enhanced Appendix B with real NYCT decline memo examples and refined format requirements