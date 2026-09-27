# Intent Routing with TypeSafe's JEV Model

AI-powered **intent classification** for customer support conversations. It identifies the customer's primary intent from a free-text message, returning a structured result with confidence scores and probability distributions so downstream systems can route the conversation appropriately.

Routing decisions remain configurable; the tool provides probabilistic intent detection, not hardcoded rules.


## Run locally

```bash
uv run python main.py
```


## What the code does

The code orchestrates a single-step intent classification using TypeSafe's JEV (Judgmental Evaluation of Values) model through the `typesafe-sdk`. Given a customer message, it returns a structured intent classification composed of:

- **`intent`** — The identified intent label from a predefined set (e.g., `order_status`, `delivery_tracking`, `payment_refund`).
- **`confidence`** — A probability score (0.0–1.0) indicating the model's certainty in the classification.
- **`requires_clarification`** — A boolean flag set to `true` when confidence is below 0.8, signaling the need for follow-up questions.
- **`probabilities`** — A dictionary mapping each possible intent to its probability score, enabling downstream fallback logic.


### Supported Intents

| Intent | Description |
|--------|-------------|
| `order_status` | The customer wants to know the status of an order. |
| `order_cancel` | The customer wants to cancel an order. |
| `delivery_tracking` | The customer wants to track a delivery or discover where the order is. |
| `delivery_delayed` | The customer says the delivery is delayed. |
| `delivery_address_change` | The customer wants to change the delivery address. |
| `payment_failed` | The payment failed or was declined. |
| `payment_refund` | The customer wants a refund. |
| `product_information` | The customer wants information about a product. |
| `product_availability` | The customer wants to know whether a product is available. |
| `return_request` | The customer wants to return a product. |
| `return_status` | The customer wants to know the status of a return. |
| `unknown` | The message does not clearly match any other intent. |


### Example

**Input message:** `"I want to know where is my order"`

**Output:**

```python
IntentResult(
    intent='delivery_tracking',
    confidence=0.92,
    requires_clarification=False,
    probabilities={
        'delivery_tracking': 0.92,
        'order_status': 0.05,
        'delivery_delayed': 0.02,
        'order_cancel': 0.01,
        ...
    }
)
```


## Architecture

```
main.py
  -> IntentClassifier.classify(message)
     -> TypeSafeClient.system_one()
        -> JEV Model (OpenRouter API)
     <- IntentResult
```


### Components

1. **`domain.py`** — Pydantic models defining the intent schema and descriptions.
   - `IntentResult`: Structured output with intent, confidence, and probabilities.
   - `INTENTS`: Mapping of intent labels to human-readable descriptions.

2. **`classifier.py`** — The `IntentClassifier` class wrapping the TypeSafe SDK.
   - Uses `Choice` questions with criteria to constrain the model output.
   - Applies a confidence threshold (0.8) to flag messages needing clarification.

3. **`main.py`** — Entry point demonstrating usage.
   - Loads API credentials from environment variables.
   - Classifies a sample message and prints the result.


## Configuration

Create a `.env` file with your OpenRouter API key:

```bash
OPENROUTER_API_KEY=sk-or-v1-...
```


## Dependencies

- `python-dotenv` — Environment variable management.
- `typesafe-sdk` — TypeSafe SDK for structured LLM interactions.


## Extending the classifier

1. **Add new intents:**
   - Update `INTENTS` dictionary in `domain.py` with the new label and description.
   - Update the `intent` Literal type in `IntentResult` to include the new label.

2. **Adjust confidence threshold:**
   - Modify the `requires_clarification` logic in `classifier.py` (default: 0.8).

3. **Add metadata extraction:**
   - Extend `IntentResult` with additional fields (e.g., `order_id`, `product_name`).
   - Add corresponding `Choice` or extraction questions to the `system_one()` call.


## TODO List

- [ ] Add multi-turn conversation context for improved intent disambiguation.
- [ ] Implement intent-specific entity extraction (order IDs, tracking numbers, etc.).
- [ ] Add evaluation dataset with labeled examples for regression testing.
- [ ] Support confidence calibration for production monitoring.
