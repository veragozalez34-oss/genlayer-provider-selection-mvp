# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json
import typing


class SeniorProgramProviderSelection(gl.Contract):
    # Program requirements
    program_name: str
    district: str
    activity_type: str
    required_capacity: u256
    required_slots_text: str
    must_have_requirements: str

    # Resolution result
    has_resolved: bool
    winner_index: i32
    winner_name: str
    winner_reason: str

    # Provider storage (DO NOT initialize manually)
    provider_names: DynArray[str]
    provider_districts: DynArray[str]
    provider_activity_types: DynArray[str]
    provider_capacities: DynArray[u256]
    provider_slots_texts: DynArray[str]
    provider_instructor_summaries: DynArray[str]
    provider_program_descriptions: DynArray[str]
    provider_equipment_descriptions: DynArray[str]
    provider_extra_activities: DynArray[str]

    def __init__(
        self,
        program_name: str,
        district: str,
        activity_type: str,
        required_capacity: u256,
        required_slots_text: str,
        must_have_requirements: str,
    ):
        self.program_name = program_name
        self.district = district
        self.activity_type = activity_type
        self.required_capacity = required_capacity
        self.required_slots_text = required_slots_text
        self.must_have_requirements = must_have_requirements

        self.has_resolved = False
        self.winner_index = i32(-1)
        self.winner_name = ""
        self.winner_reason = ""

    @gl.public.write
    def submit_provider(
        self,
        provider_name: str,
        provider_district: str,
        provider_activity_type: str,
        provider_capacity: u256,
        provider_slots_text: str,
        instructor_summary: str,
        program_description: str,
        equipment_description: str,
        extra_activities: str,
    ) -> None:
        if self.has_resolved:
            raise gl.vm.UserError("Selection already resolved")

        self.provider_names.append(provider_name)
        self.provider_districts.append(provider_district)
        self.provider_activity_types.append(provider_activity_type)
        self.provider_capacities.append(provider_capacity)
        self.provider_slots_texts.append(provider_slots_text)
        self.provider_instructor_summaries.append(instructor_summary)
        self.provider_program_descriptions.append(program_description)
        self.provider_equipment_descriptions.append(equipment_description)
        self.provider_extra_activities.append(extra_activities)

    @gl.public.view
    def get_provider_count(self) -> u256:
        return u256(len(self.provider_names))

    @gl.public.view
    def list_providers(self) -> str:
        providers = []
        count = len(self.provider_names)

        for i in range(count):
            providers.append(
                {
                    "index": i,
                    "provider_name": self.provider_names[i],
                    "provider_district": self.provider_districts[i],
                    "provider_activity_type": self.provider_activity_types[i],
                    "provider_capacity": int(self.provider_capacities[i]),
                    "provider_slots_text": self.provider_slots_texts[i],
                    "instructor_summary": self.provider_instructor_summaries[i],
                    "program_description": self.provider_program_descriptions[i],
                    "equipment_description": self.provider_equipment_descriptions[i],
                    "extra_activities": self.provider_extra_activities[i],
                }
            )

        return json.dumps(providers)

    @gl.public.view
    def get_eligible_providers(self) -> str:
        eligible = []
        count = len(self.provider_names)

        for i in range(count):
            if self._is_eligible(i):
                eligible.append(
                    {
                        "index": i,
                        "provider_name": self.provider_names[i],
                        "provider_district": self.provider_districts[i],
                        "provider_activity_type": self.provider_activity_types[i],
                        "provider_capacity": int(self.provider_capacities[i]),
                        "provider_slots_text": self.provider_slots_texts[i],
                        "instructor_summary": self.provider_instructor_summaries[i],
                        "program_description": self.provider_program_descriptions[i],
                        "equipment_description": self.provider_equipment_descriptions[i],
                        "extra_activities": self.provider_extra_activities[i],
                    }
                )

        return json.dumps(eligible)

    @gl.public.write
    def resolve_best_provider(self) -> str:
        if self.has_resolved:
            raise gl.vm.UserError("Selection already resolved")

        eligible = []
        count = len(self.provider_names)

        for i in range(count):
            if self._is_eligible(i):
                eligible.append(
                    {
                        "index": i,
                        "provider_name": self.provider_names[i],
                        "provider_district": self.provider_districts[i],
                        "provider_activity_type": self.provider_activity_types[i],
                        "provider_capacity": int(self.provider_capacities[i]),
                        "provider_slots_text": self.provider_slots_texts[i],
                        "instructor_summary": self.provider_instructor_summaries[i],
                        "program_description": self.provider_program_descriptions[i],
                        "equipment_description": self.provider_equipment_descriptions[i],
                        "extra_activities": self.provider_extra_activities[i],
                    }
                )

        if len(eligible) == 0:
            raise gl.vm.UserError("No eligible providers found")

        program_name = self.program_name
        district = self.district
        activity_type = self.activity_type
        required_capacity = int(self.required_capacity)
        required_slots_text = self.required_slots_text
        must_have_requirements = self.must_have_requirements
        eligible_json = json.dumps(eligible)

        def ask_llm() -> typing.Any:
            prompt = f"""
You are evaluating providers for a senior wellness community program.

PROGRAM REQUIREMENTS
- Program Name: {program_name}
- District: {district}
- Activity Type: {activity_type}
- Required Capacity: {required_capacity}
- Required Slots: {required_slots_text}
- Must-have Requirements: {must_have_requirements}

All providers below already passed the hard filter:
- district match
- activity type match
- capacity >= required capacity

Choose the SINGLE BEST provider using these qualitative criteria:
1. Program fit for adults 55+
2. Instructor relevance for older adults
3. Equipment suitability and safety
4. Added community value
5. Penalize vague, overly intense, or poorly suited offerings

ELIGIBLE PROVIDERS (JSON):
{eligible_json}

Return ONLY valid JSON:
{{
  "winner_index": <integer>,
  "winner_name": "<exact provider name>",
  "winner_reason": "<short explanation>"
}}
"""
            raw = gl.nondet.exec_prompt(prompt)
            cleaned = raw.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)

        result = gl.eq_principle.strict_eq(ask_llm)

        winner_index = int(result["winner_index"])
        winner_name = str(result["winner_name"])
        winner_reason = str(result["winner_reason"])

        matched = False
        for item in eligible:
            if int(item["index"]) == winner_index:
                if str(item["provider_name"]) != winner_name:
                    raise gl.vm.UserError("winner_name does not match winner_index")
                matched = True
                break

        if not matched:
            raise gl.vm.UserError("winner_index not in eligible shortlist")

        self.has_resolved = True
        self.winner_index = i32(winner_index)
        self.winner_name = winner_name
        self.winner_reason = winner_reason

        return json.dumps(
            {
                "winner_index": winner_index,
                "winner_name": winner_name,
                "winner_reason": winner_reason,
            }
        )

    @gl.public.view
    def get_selection_result(self) -> str:
        return json.dumps(
            {
                "has_resolved": self.has_resolved,
                "winner_index": int(self.winner_index),
                "winner_name": self.winner_name,
                "winner_reason": self.winner_reason,
            }
        )

    def _is_eligible(self, i: int) -> bool:
        district_ok = self.provider_districts[i].strip().lower() == self.district.strip().lower()
        activity_ok = self.provider_activity_types[i].strip().lower() == self.activity_type.strip().lower()
        capacity_ok = int(self.provider_capacities[i]) >= int(self.required_capacity)

        return district_ok and activity_ok and capacity_ok
