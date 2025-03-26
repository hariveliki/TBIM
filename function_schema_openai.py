tools = [
    {
        "type": "function",
        "function": {
            "name": "query_space_property",
            "description": "Query a property from a specific space type in the topologic graph.",
            "parameters": {
                "type": "object",
                "properties": {
                    "space_type": {
                        "type": "string",
                        "description": "Occupancy type of the space (e.g. Toilet, Corridor)",
                    },
                    "property_key": {
                        "type": "string",
                        "enum": [
                            "pr_AreaPerOccupantPeak",
                            "pr_AtmosphereType",
                            "pr_CirculationType",
                            "pr_EquipmentPowerDensity",
                            "pr_HumidityMax",
                            "pr_HumidityMin",
                            "pr_Illuminance",
                            "pr_IsCooled",
                            "pr_IsHeated",
                            "pr_IsMechanicallyVentilated",
                            "pr_IsNaturallyVentilated",
                            "pr_IsOccupied",
                            "pr_LightingPowerDensity",
                            "pr_MechanicalVentilationPerArea",
                            "pr_MechanicalVentilationRate",
                            "pr_NaturalVentilationPerArea",
                            "pr_NaturalVentilationRate",
                            "pr_OccupancyNumberPeak",
                            "pr_OccupancyType",
                            "pr_OccupancyType_Number",
                            "pr_Occupant",
                            "pr_PrivacyType",
                            "pr_SpaceTemperatureSummerMax",
                            "pr_SpaceTemperatureSummerMin",
                            "pr_SpaceTemperatureWinterMax",
                            "pr_SubOccupant",
                        ],
                        "description": "One of the allowed property keys for querying",
                    },
                },
                "required": ["space_type", "property_key"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]
