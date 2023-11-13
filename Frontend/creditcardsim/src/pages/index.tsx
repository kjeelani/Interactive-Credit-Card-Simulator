import Head from 'next/head'
import Image from 'next/image'
import { Inter } from '@next/font/google'
import styles from '@/styles/Home.module.css'
import { ChakraProvider } from '@chakra-ui/react'
import { UserLogin } from '@/components/UserLogin'
import { CreditSim } from '@/components/CreditSim'
import { useEffect, useState } from 'react'
import { 
  Text, 
  Heading
} from '@chakra-ui/react'
import axios from 'axios';


const inter = Inter({ subsets: ['latin'] })

export default function Home() {
  const [userID, setUserID] = useState("")
  const [userData, setUserData] = useState("")
  const [loading, setLoading] = useState(false);
  
  const fetchData = async (userID: string) => {
    try {
      setLoading(true)
      const response = await axios.get('http://127.0.0.1:8080/user/' + userID); // Replace with your API endpoint
      setUserData(response.data["data"]);
    } finally {
      setLoading(false);
    }
  };
  

  useEffect(() => {
    if (userID !== "") {
      fetchData(userID)
    }
  }, [userID]);


  return (
    <ChakraProvider>
      <Head>
        <title>Credit Card Sim</title>
        <meta name="description" content="Pomelo Inspired App" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Heading textAlign="center" font-size="xl">Interactive Credit Card Simulator</Heading>
      <div className="center_wrap">
          {
            userData === "" 
            ?
            <UserLogin 
              userID={userID} 
              setUserID={setUserID}
            />
            :
            <CreditSim 
              userID={userID} 
              setUserID={setUserID}
              userData={userData}
              setUserData={setUserData}
            />
          }   
          {
            loading ?
            <Text>Loading...</Text> :
            <Text></Text>
          }
      </div>
    </ChakraProvider>
  )
}
