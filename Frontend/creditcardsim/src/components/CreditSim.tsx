import React, { useEffect, useState } from "react";
import { 
    Input,
    InputGroup,
    InputLeftAddon,
    Button,
    FormControl,
    FormHelperText,
    FormLabel,
    HStack,
    Text,
    Select,
    VStack,
    Heading
} from '@chakra-ui/react'
import axios from "axios";


export interface CreditSimProps {
	userID: string,
    setUserID: any,
    userData: string,
    setUserData: any
}

interface EventType {
    eventType: string,
    eventTime: Date,
    txnId: string,
    amount: string
}

export function CreditSim(props: CreditSimProps) {
    const [eventID, setEventID] = useState("txn1")
    const [eventType, setEventType] = useState("TXN_AUTHED")
    const [amount, setAmount] = useState("0")
    const [hasSubmitted, setHasSubmitted] = useState(false)
    const [loading, setLoading] = useState(false)

    
    useEffect(() => {
        if (hasSubmitted) {
            let txnEvent = {
                "eventType": eventType,
                "eventTime": Date.now(),
                "txnId": eventID,
                "amount": parseInt(amount)
            }
            setLoading(true)
            const fetchData = async () => {
                // Replace 'https://your-api-endpoint' with the actual URL of your API
                const api_url = 'http://127.0.0.1:8080/user/' + props.userID;
                const response = await axios.put(api_url, {"event": txnEvent});
        
                // Handle the response data as needed
                props.setUserData(response.data["data"]);
            }
            fetchData()
            setLoading(false)
            setHasSubmitted(false)
        }   
    }, [hasSubmitted])

    

    return (
        <>
            <FormControl as='fieldset'>
                <VStack spacing="2">
                    <FormLabel as='legend'>
                        Create New Event
                    </FormLabel>
                    <InputGroup maxW="50vw">
                        <InputLeftAddon children='Transaction ID: ' />
                        <Input 
                            placeholder='txn1' 
                            onChange={(e) => {
                                setEventID(e.target.value)
                            }}
                        />
                    </InputGroup>
                    <FormLabel>Event Details</FormLabel>
                    <Select 
                        maxW="50vw"
                        onChange={(e) => {
                            setEventType(e.target.value)
                        }}
                    >
                        <option value='TXN_AUTHED'>New Transaction</option>
                        <option value='TXN_AUTH_CLEARED'>Clear Transaction</option>
                        <option value='TXN_SETTLED'>Settle Transaction</option>
                        <option value='PAYMENT_INITIATED'>New Payment</option>
                        <option value='PAYMENT_CANCELED'>Cancel Payment</option>
                        <option value='PAYMENT_POSTED'>Post Payment</option>
                    </Select>
                    <InputGroup maxW="50vw">
                        <InputLeftAddon children='Amount: ' />
                        <Input 
                            placeholder='0' 
                            onChange={(e) => {
                                setAmount(e.target.value)
                            }}
                        />
                    </InputGroup>
                    <HStack spacing="4">
                        <Button 
                            w="16vh"
                            type="submit"
                            backgroundColor="blue.300"
                            _hover={{ bg: "blue.400" }}
                            onClick={() => {
                                /* Update Data */
                                setHasSubmitted(true)
                            }}
                        >
                            Submit
                        </Button>
                        <Button 
                            w="16vh"
                            type="submit"
                            backgroundColor="red.500"
                            _hover={{ bg: "red.600" }}
                            onClick={() => {
                                /* Reset Everything */
                                props.setUserID("")
                                props.setUserData("")
                            }}
                        >
                            Sign Out
                        </Button>
                    </HStack>
                    <Heading mt="4vh">Transaction Summary</Heading>
                    <Text fontSize="lg" textAlign={"center"}>{loading ? "Loading..." : props.userData}</Text>
                </VStack>
            </FormControl>
        </>
    );
}