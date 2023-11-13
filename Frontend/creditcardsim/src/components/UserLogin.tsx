import React, { useState } from "react";
import { 
    Input,
    InputGroup,
    InputLeftAddon,
    Button,
    VStack
} from '@chakra-ui/react'


export interface UserLoginProps {
	userID: string,
    setUserID: any
}

export function UserLogin(props: UserLoginProps) {
    const [currentUserID, setCurrentUserID] = useState("id1")

    return (
        <VStack>
            <InputGroup maxW="50vw">
                <InputLeftAddon children='Enter UserID: ' />
                <Input 
                    placeholder='id1' 
                    onChange={(e) => {
                        setCurrentUserID(e.target.value)
                    }}
                />
            </InputGroup>
            <Button 
                w="16vh"
                type="submit"
                backgroundColor="blue.300"
                _hover={{ bg: "blue.400" }}
                onClick={() => {
                    props.setUserID(currentUserID)
                }}
            >   
                Sign In
            </Button>
        </VStack>
    );
}