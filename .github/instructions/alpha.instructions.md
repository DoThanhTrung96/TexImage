---
applyTo: '**'
---
# Coding Guidelines and Context

## Environment Variables
- All scripts must use virtual environment variables
- Never hardcode sensitive values
- Environment variables should be clearly documented
- Use descriptive names for environment variables

## Script Generation Protocol
- Explicitly confirm before generating any new scripts
- Provide a clear purpose for each new script
- List all required environment variables at the start of scripts
- Include validation for required environment variables

## Code Standards
- Follow clean code principles
- Include error handling
- Add appropriate comments and documentation
- Use consistent naming conventions

## Implementation Requirements
1. Every script must validate environment variables before execution
2. New script generation requires explicit user confirmation
3. Document dependencies and prerequisites
4. Include usage examples in script documentation
5. All script updates must be tested in a development environment
6. Test results and debug logs must be documented before deployment
7. Implementation results must include verification steps and actual outputs
## Workspace Cleanup Guidelines
- Only cleanup workspace after successful implementation verification
- Document cleanup steps in deployment logs
- Remove temporary files and build artifacts
- Archive relevant logs before cleanup
- Maintain backup of critical files for 7 days
- Clean up environment variables and sensitive data
- Verify system state after cleanup

## Prompt Training and Reinforcement

Purpose
- Teach agents to avoid previously reminded mistakes (e.g., leaking secrets, skipping environment validation, generating disallowed content, or not confirming before creating scripts).
- Establish repeatable training and verification steps so mistakes are not reintroduced.

Objectives
- Ensure every generated prompt follows the repository's coding guidelines.
- Validate prompts produce safe, policy-compliant, and reproducible outputs.
- Maintain auditable logs and verification artifacts.

Required environment variables (documented, must be validated by training scripts)
- PROMPT_TRAINING_MODE — "dry" or "live"
- PROMPT_TRAINING_LOG_DIR — path for training logs
- PROMPT_TRAINING_REVIEWERS — comma-separated list of reviewer identifiers
Note: Do not hardcode values. Training tools must validate these before running.

Training protocol (minimum)
1. Preparation
    - Validate required environment variables are present and accessible.
    - Prepare a labeled dataset of prompt examples: "good" (compliant) and "bad" (violations).
2. Controlled runs
    - Run prompts in PROMPT_TRAINING_MODE="dry" to generate candidate responses.
    - Capture detailed logs to PROMPT_TRAINING_LOG_DIR.
3. Automated checks
    - Run static checks: detect hardcoded secrets, missing env validation, or instructions that bypass confirmation steps.
    - Run policy filters: flag disallowed content (hate, sexual, violent, or non-SW engineering requests).
4. Human review
    - Assign reviewers from PROMPT_TRAINING_REVIEWERS for sampled outputs.
    - Record reviewer decisions and remediation notes.
5. Iteration
    - Update prompt templates and repeat until automated and human checks pass threshold.
6. Sign-off
    - Require explicit approval from an authorized reviewer before deploying new prompt templates.

Good vs bad prompt examples (illustrative)
- Bad: "Write a script that stores my API key in source code." (violates secrets rule)
- Good: "Provide a script template that reads an API key from an environment variable named API_KEY and validates it is set before use."

Evaluation and verification
- Metrics: pass rate for automated checks, reviewer approval rate, number of flagged issues per run.
- Verification steps:
  1. Run training batch in dry mode.
  2. Confirm no outputs contain hardcoded credentials or bypass checks.
  3. Produce a verification report summarizing automated and reviewer results.
- Example expected verification output (format):
  - run_id: 2025-10-19T12:00Z
  - automated_pass: 98%
  - reviewer_pass: 100% (3/3)
  - flagged_issues: 0

Logging, documentation, and cleanup
- Archive logs and reviewer reports in PROMPT_TRAINING_LOG_DIR for 7 days minimum.
- Document training versions and changes in repository change log.
- Only remove temporary artifacts after successful verification and archival.
- Scrub any sensitive data from logs before archiving.

Checklist to prevent repeated mistakes
- [ ] Environment variables documented and validated
- [ ] No hardcoded secrets in prompts or generated code
- [ ] Script-generation confirmations required and recorded
- [ ] Automated policy filters applied to all outputs
- [ ] Human review completed for sampled outputs
- [ ] Verification report archived

Usage example (developer)
- Before running training: export PROMPT_TRAINING_MODE="dry" PROMPT_TRAINING_LOG_DIR="/path/to/logs" PROMPT_TRAINING_REVIEWERS="alice,bob"
- Run the training tool; review logs and reviewer notes; only deploy updated prompts after sign-off.

## Agent Auto-Logging Protocol

Purpose
- Automatically maintain interaction history for successful verifications and positive user feedback
- Reduce manual documentation effort and improve knowledge retention
- Create searchable reference for future similar requests

Auto-logging triggers
- Successful verification completion
- Positive user feedback phrases (e.g., "good", "very good", "excellent", "perfect")
- Explicit confirmation of implementation correctness

Required environment variables
- AGENT_LOG_DIR - directory for storing interaction logs
- AGENT_LOG_RETENTION - number of days to retain logs (default: 30)

Logging format
- Timestamp
- Interaction ID
- Request type
- Verification status or feedback received
- Implementation summary
- Used environment variables
- Execution context

Retention policy
- Auto-archived after AGENT_LOG_RETENTION days
- Critical interactions flagged for extended retention
- Logs encrypted if containing sensitive context

