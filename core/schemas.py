from pydantic import BaseModel, Field, field_serializer, field_validator, PositiveFloat, constr

# Base schema with validations
class CostBaseSchema(BaseModel):
    description: constr(strip_whitespace=True, min_length=1, max_length=255) = Field(
        ..., description="Description of the cost"
    )
    amount: PositiveFloat = Field(
        ..., description="Amount must be a positive number"
    )

    # Optional: Ensure description doesn't contain special characters
    @field_validator("description")
    def validate_description(cls, v):
        import re
        if not re.match(r"^[\w\s.,'-]+$", v):
            raise ValueError("Description contains invalid characters")
        return v


# Schema for creating a cost (inherits validation from base)
class CostCreateSchema(CostBaseSchema):
    pass


# Response schema with ID and serialized amount
class CostResponseSchema(CostBaseSchema):
    id: int = Field(..., description="Unique cost identifier")

    @field_serializer("amount")
    def serialize_amount(self, value: float) -> float:
        # round to 2 decimal places for response
        return round(value, 2)


# Schema for updating a cost (all fields optional)
class CostUpdateSchema(BaseModel):
    description: constr(strip_whitespace=True, min_length=5, max_length=255) | None = Field(
        None, description="Updated description of the cost"
    )
    amount: PositiveFloat | None = Field(
        None, description="Updated amount must be positive"
    )

    @field_validator("description")
    def validate_description(cls, v):
        if v is None:
            return v
        import re
        if not re.match(r"^[\w\s.,'-]+$", v):
            raise ValueError("Description contains invalid characters")
        return v
