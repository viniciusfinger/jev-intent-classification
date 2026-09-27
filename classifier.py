from typesafe_sdk import TypeSafeClient, Choice
from domain import IntentResult, INTENTS


class IntentClassifier:
    def __init__(self, client: TypeSafeClient):
        self.client = client

    def classify(self, message: str) -> IntentResult:
        response = self.client.system_one(
            state={
                "message": message
            },
            questions={
                "intent": Choice(
                    instructions="Identify the customer's primary intent.",
                    criteria=INTENTS
                )
            }
        )

        result = response.choices["intent"]
        requires_clarification = result.confidence < 0.8

        return IntentResult(
            intent=result.choice,
            confidence=result.confidence,
            probabilities=result.probabilities,
            requires_clarification=requires_clarification
        )
